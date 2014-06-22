from flask.ext import restful
from flask.ext.restful import fields, marshal_with, reqparse

class Link(restful.Resource):
    def get(self):
        return "hi"
