from flask.ext import restful
from flask.ext.restful import fields, marshal_with, reqparse

class Contacts(restful.Resource):
    def get(self):
        return "hi"

class Contact(restful.Resource):
    def get(self):
        return "hi"
