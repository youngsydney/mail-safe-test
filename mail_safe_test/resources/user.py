from flask import request, jsonify, Response, abort
from flask.ext import restful
from flask.ext.restful import fields, marshal_with, reqparse
from flask_ndb_api import NDBJSONEncoder
from google.appengine.ext import ndb
from mail_safe_test.errors import HTTP_Error
from mail_safe_test import app
from flask.ext.restful import reqparse

class UserModel(ndb.Model):
    # id - in this key
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()
    oauth = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)


class UserAPI(restful.Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('first_name', type = str, location = 'json')
        self.reqparse.add_argument('last_name', type = str, location = 'json')
        self.reqparse.add_argument('email', type = str, required=True, location = 'json')
        self.reqparse.add_argument('Authorization', type=str, required=True, location='headers',
                                    dest='oauth')
        super(UserAPI, self).__init__()

    def _get_user(self, request):
        # TODO(gdb): Verify authorization header
        user_id = request.headers.get('Authorization')
        if user_id is None:
            abort(400)
        user_key = ndb.Key(UserModel, user_id)
        user_obj = user_key.get()
        return user_obj

    # login_required    
    def get(self):
        # expose a single user
        user_obj = self._get_user(request)
        if user_obj is None:
            abort(404)
        return jsonify(user_obj)

    # login_required    
    def post(self):
        # create a new user
        args = self.reqparse.parse_args()

        return "Not Implemented", 501

    # login_required    
    def put(self):
        # update a single user
        return "Not Implemented", 501

    # login_required    
    def delete(self):
        # delete a single user
        return "Not Implemented", 501
