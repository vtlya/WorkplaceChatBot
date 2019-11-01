import json
import six

from pymessenger.bot import Bot


class Buts(dict):
    __acceptable_keys = ['content_type', 'title', 'payload', 'image_url']
    def __init__(self, *args, **kwargs):
        if six.PY2:
            kwargs = {k:v for k, v in kwargs.iteritems() if k in self.__acceptable_keys}
        else:
            kwargs = {k:v for k, v in kwargs.items() if k in self.__acceptable_keys}
        super(Buts, self).__init__(*args, **kwargs)

    def to_json(self):
        return json.dumps({k:v for k, v in self.iteritems() if k in self.__acceptable_keys})
