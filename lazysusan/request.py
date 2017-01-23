from datetime import datetime


class Request(object):

    def __init__(self, request):
        self._request = request

    @property
    def intent_name(self):
        try:
            return self._request["intent"]["name"]
        except KeyError:
            pass

        try:
            return self._request["type"]
        except KeyError:
            pass

        raise Exception("Could not find appropriate callback for intent: %s" % (self._request, ))

    @property
    def raw(self):
        return self._request

    @property
    def request_type(self):
        return self._request["type"]

    @property
    def timestamp(self):
        return datetime.strptime(self._request["timestamp"], "%Y-%m-%dT%H:%M:%SZ")

    def get_slot_value(self, slot_name):
        try:
            return self._request["intent"]["slots"][slot_name]["value"]
        except KeyError:
            pass
