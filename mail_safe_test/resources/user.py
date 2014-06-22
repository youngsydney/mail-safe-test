from flask.ext import restful
from flask.ext.restful import fields, marshal_with, reqparse

class Users(restful.Resource):
    def get(self):
        return "hi noone"

class User(restful.Resource):
    def get(self, user_id):
        return "hi %d"%(user_id)
