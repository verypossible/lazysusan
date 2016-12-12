import os
import persistence


from datetime import datetime


class Session(object):

    def __init__(self, user_id, session_key, event=None):
        self._user_id = user_id

        self.__event = event or {}
        self._backend = self.get_backend()
        self._backend.connect(userId=self._user_id)
        self.__session_key = session_key

    @property
    def is_expired(self):
        try:
            time_limit = int(os.environ.get("LAZYSUSAN_TTL_SECONDS", "0"))
        except ValueError:
            raise ValueError("The LAZYSUSAN_TTL_SECONDS must be an integer greater than 0")

        if time_limit <= 0:
            return False

        return (datetime.now() - self.last_request_time).total_seconds() > time_limit

    @property
    def last_request_time(self):
        return self.get("LAST_REQUEST_TIME", datetime.now())

    @last_request_time.setter
    def last_request_time(self, timestamp):
        self.set("LAST_REQUEST_TIME", timestamp)

    def get(self, key, default=None):
        return self._backend.get(key, default)

    def set(self, key, val):
        self._backend[key] = val

    def clear(self):
        self._backend.clear()
        self._backend["userId"] = self._user_id

    def get_backend(self):
        backend = os.environ.get("LAZYSUSAN_SESSION_STORAGE_BACKEND", "dynamodb")

        if backend == "dynamodb":
            return persistence.DynamoDB()
        elif backend == "cookie":
            try:
                memory = persistence.Memory()
                memory.update(self.__event["session"]["attributes"])
                return memory
            except (KeyError, TypeError), err:
                pass

        return persistence.Memory()

    def get_state(self):
        return self._backend.get(self.__session_key, "initialState")

    def get_state_params(self):
        return {self.__session_key: self.get_state()}

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
