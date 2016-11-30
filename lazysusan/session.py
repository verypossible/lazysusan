import os
import persistence


class Session(object):

    def __init__(self, user_id, session_key):
        self._user_id = user_id

        self._backend = self.get_backend()
        self._backend.connect(userId=self._user_id)
        self.__session_key = session_key

    def get_backend(self):
        backend = os.environ.get("LAZYSUSAN_SESSION_STORAGE_BACKEND", "dynamodb")

        if backend == "dynamodb":
            return persistence.DynamoDB()
        else:
            return persistence.Memory()

    def get_state(self):
        return self._backend.get(self.__session_key, "initialState")

    def get_audio_offset(self):
        try:
            return self._backend["AudioPlayer"]["offsetInMilliseconds"]
        except (KeyError, TypeError), err:
            return 0

    def update_audio_state(self, context):
        # context may be None in certain requests. In that case we may just pass
        try:
            self._backend["AudioPlayer"] = context["AudioPlayer"]
        except (KeyError, TypeError), err:
            pass

    def update_state(self, state, context):
        self._backend.update({
            self.__session_key: state,
            "userId": self._user_id,
        })
        self.update_audio_state(context)

    def save(self):
        self._backend.save()
