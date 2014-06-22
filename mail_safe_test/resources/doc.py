from flask.ext import restful
from flask.ext.restful import fields, marshal_with, reqparse

class Docs(restful.Resource):
    def get(self):
        return "hi"

class Doc(restful.Resource):
    def get(self):
        return "hi"
