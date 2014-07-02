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
}

parser = reqparse.RequestParser()
parser.add_argument('first_name', type = str, location = 'json')
parser.add_argument('last_name', type = str, location = 'json')
parser.add_argument('email', type = str, location = 'json')
parser.add_argument('Authorization', type=str, required=True, location='headers',
                            dest='oauth')

class UserModel(ndb.Model):
    # id - in this key
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()
    oauth = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    last_active = ndb.DateTimeProperty(auto_now_add=True)

def get_user(request):
    # TODO(gdb): Verify authorization header
    user_id = request.headers.get('Authorization')
    if user_id is None:
        abort(400)
    user_key = ndb.Key(UserModel, user_id)
    user_obj = user_key.get()
    return user_obj

class AdminUserAPI(restful.Resource):
    '''GET, PUT, DELETE on _other_ users'''
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
    user_list_fields = {'users': fields.List(fields.Nested(user_fields))}

    @marshal_with(user_list_fields)
    def get(self):
        user_objs = UserModel.query().fetch()
        return {'users': user_objs}

    @marshal_with(user_list_fields)
    def delete(self):
        ndb.delete_multi(UserModel.query().fetch(keys_only=True))
        user_objs = UserModel.query().fetch()
        return {'users': user_objs}


class UserListAPI(restful.Resource):
    def __init__(self):
        self.parser = parser.copy()
        self.parser.replace_argument('email', type = str, required = True, location = 'json')
        super(UserListAPI, self).__init__()

    @marshal_with(user_fields)
    def post(self):
        # create a new user
        print request.get_json()
        args = self.parser.parse_args()
        user_obj = UserModel(**args)
        user_obj.put()
        return user_obj

class UserAPI(restful.Resource):
    def __init__(self):
        self.parser = parser.copy()
        super(UserAPI, self).__init__()

    @marshal_with(user_fields)
    def get(self):
        user_obj = get_user(request)
        if user_obj is None:
            abort(404)
        return user_obj

    @marshal_with(user_fields)
    def put(self):
        # update a single user
        abort(501)

    def delete(self):
        # delete a single user
        abort(501)
