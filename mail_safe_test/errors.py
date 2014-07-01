# errors.py
class HTTP_Error(Exception):
    status_code = 400

    def __init__(self, message, status=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status is not None:
            self.status_code = status
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.message
        return rv
