import flask
from flask import request, Response, abort, make_response
from flask.ext import restful
from flask.ext.restful import fields, marshal, marshal_with, reqparse
import flask_restful
from flask_ndb_api import NDBJSONEncoder, ndbdumps, entity_to_dict
from google.appengine.ext import ndb
import json
from urlparse import urlparse, urlunparse
from mail_safe_test.errors import HTTP_Error
from mail_safe_test import app

class NDBUrl(fields.Url):
    def output(self, key, obj):
        try:
            data = obj.to_dict()
            data['key'] = obj.key.urlsafe()
            data['key_id'] = obj.key.id()
            o = urlparse(flask.url_for(self.endpoint, _external=self.absolute, **data))
            if self.absolute:
                scheme = self.scheme if self.scheme is not None else o.scheme
                return urlunparse((scheme, o.netloc, o.path, "", "", ""))
            return urlunparse(("", "", o.path, "", "", ""))
        except TypeError as te:
            raise MarshallingException(te)

# Public exports
user_fields = {
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'created': fields.DateTime,
    'last_active': fields.DateTime,
    'uri': NDBUrl('/admin/user/'),
#    'uri': NDBUrl('/user/'),
}

parser = reqparse.RequestParser()
parser.add_argument('first_name', type = str, location = 'json')
parser.add_argument('last_name', type = str, location = 'json')
parser.add_argument('email', type = str, location = 'json')
parser.add_argument('Authorization', type=str, required=True, location='headers',
                            dest='oauth')

class UserModel(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()
    oauth = ndb.StringProperty()
    admin = ndb.BooleanProperty(default=False)
    created = ndb.DateTimeProperty(auto_now_add=True)
    last_active = ndb.DateTimeProperty(auto_now_add=True)

def get_user(request):
    # TODO(gdb): Verify authorization header loop up user.
    user_id = request.headers.get('Authorization')
    if not user_id or not user_id.isdigit():
        abort(400)
    key_id = int(user_id)
    return ndb.Key(UserModel, key_id).get()

from functools import wraps
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_user = get_user(request)
        print "authuser", auth_user
        if not auth_user or not auth_user.admin:
            abort(403)
        return func(*args, **kwargs)
    return wrapper

class AdminUserAPI(restful.Resource):
    '''GET, PUT, DELETE on _other_ users'''
    method_decorators = [admin_required]

    @marshal_with(user_fields)
    def get(self, key_id):
        user = ndb.Key(UserModel, key_id).get()
        if not user:
            abort(404)
        return user

    @marshal_with(user_fields)
    def put(self, key_id):
        user = ndb.Key(UserModel, key_id).get()
        if not user:
            abort(404)
        args = parser.parse_args()
        user.populate(**args)
        user.put()
        return user

    def delete(self, key_id):
        key = ndb.Key(UserModel, key_id)
        if not key.get():
            abort(404)
        key.delete()
        return make_response("", 204)

class AdminUserListAPI(restful.Resource):
    method_decorators = [admin_required]
    user_list_fields = {'users': fields.List(fields.Nested(user_fields))}

    @marshal_with(user_list_fields)
    def get(self):
        users = UserModel.query().fetch()
        return {'users': users}

    @marshal_with(user_list_fields)
    def delete(self):
        ndb.delete_multi(UserModel.query().fetch(keys_only=True))
        users = UserModel.query().fetch()
        return {'users': users}

class UserAPI(restful.Resource):
    def __init__(self):
        self.post_parser = parser.copy()
        self.post_parser.replace_argument('email', type = str, required = True, location = 'json')
        self.put_parser = parser.copy()
        super(UserAPI, self).__init__()

    @marshal_with(user_fields)
    def get(self):
        user = get_user(request)
        if user is None:
            abort(404)
        return user

    @marshal_with(user_fields)
    def post(self):
        user = get_user(request)
        if user is not None:
            abort(403)
        args = self.post_parser.parse_args()
        user = UserModel(**args)
        user.put()
        return user

    @marshal_with(user_fields)
    def put(self):
        user = get_user(request)
        if not user:
            abort(404)
        args = self.put_parser.parse_args()
        user.populate(**args)
        user.put()
        return user

    def delete(self):
        user = get_user(request)
        # delete a single user
        if not user:
            abort(404)
        user.key.delete()
        return make_response("", 204)
