from flask import request, Response, abort, make_response, url_for
from flask.ext.restful import Resource, fields, marshal, marshal_with, reqparse
from google.appengine.ext import ndb
from mail_safe_test.custom_fields import NDBUrl
from mail_safe_test.auth import user_required, admin_required

# Public exports
user_fields = {
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'created': fields.DateTime,
    'last_active': fields.DateTime,
    'uri': NDBUrl('/user/'),
}

admin_user_fields = user_fields
admin_user_fields['uri'] = NDBUrl('/admin/user/'),

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

class AdminUserAPI(Resource):
    '''GET, PUT, DELETE on _other_ users'''
    method_decorators = [admin_required]

    @marshal_with(admin_user_fields)
    def get(self, key_id):
        user = ndb.Key(UserModel, key_id).get()
        if not user:
            abort(404)
        return user

    @marshal_with(admin_user_fields)
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

class AdminUserListAPI(Resource):
    method_decorators = [admin_required]
    user_list_fields = {'users': fields.List(fields.Nested(admin_user_fields))}

    @marshal_with(user_list_fields)
    def get(self):
        users = UserModel.query().fetch()
        return {'users': users}

    @marshal_with(user_list_fields)
    def delete(self):
        ndb.delete_multi(UserModel.query().fetch(keys_only=True))
        users = UserModel.query().fetch()
        return {'users': users}

class UserAPI(Resource):
    method_decorators = [user_required]
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
