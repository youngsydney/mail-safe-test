#custom_fields.py
from flask.ext.restful import fields

class NDBUrl(fields.Url):
    '''Extends fields.Url with the key and key_id of an NDB object.
    This allows auto-discovery and generation of paths to get/post/put/delete functions
    that accept key or key_id as arguments'''
    def output(self, key, obj):
        try:
            data = obj.to_dict()
            data['key'] = obj.key.urlsafe()
            data['key_id'] = obj.key.id()
            o = urlparse(url_for(self.endpoint, _external=self.absolute, **data))
            if self.absolute:
                scheme = self.scheme if self.scheme is not None else o.scheme
                return urlunparse((scheme, o.netloc, o.path, "", "", ""))
            return urlunparse(("", "", o.path, "", "", ""))
        except TypeError as te:
            raise MarshallingException(te)

