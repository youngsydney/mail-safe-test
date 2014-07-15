"""
doc.py

"""

from flask import request, Response, abort, make_response
from flask.ext.restful import Resource, fields, marshal_with, reqparse
from google.appengine.ext import ndb
from mail_safe_test.custom_fields import NDBUrl
from mail_safe_test.auth import current_user, user_required, admin_required, UserModel

#   public exports
doc_fields = {
    'content': fields.String,
    'date': fields.DateTime,
    'status': fields.String,
    'uri': NDBUrl('/user/doc/')
}

parser = reqparse.RequestParser()
parser.add_argument('content', type = str, location = 'json')
parser.add_argument('status', type = str, location = 'json')
parser.add_argument('Authorization', type=str, required=True, location='headers',
                            dest='oauth')

class DocModel(ndb.Model):
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    status = ndb.StringProperty()
    oauth = ndb.StringProperty()

    @classmethod
    def query_by_id(cls, user, doc_id):
        doc_key = ndb.Key(UserModel, user, DocModel, doc_id)
        return doc_key.get()

class DocList(Resource):
    method_decorators = [user_required]
    doc_list_fields = {'users': fields.List(fields.Nested(doc_fields))}

    @marshal_with(doc_list_fields)
    @user_required
    def get(self):
        docs = DocModel.query().fetch(keys_only=True))
        return {'docs': docs}

    @marshal_with(doc_list_fields)
    @user_required
    def delete(self):
        ndb.delete_multi(DocModel.query().fetch(keys_only=True))
        docs = DocModel.query().fetch()
        return {'docs': docs}

class Doc(Resource):
    def __init__(self):
        self.post_parser = parser.copy()
        self.post_parser.replace_argument(user, type = str, required = True, location = 'json')
        self.put_parser = parser.copy()
        super(DocAPI, self).__init__()

    @marshal_with(doc_fields)
    @user_required
    def get(self, doc_id):
        doc_item = DocModel.query_by_id(user, doc_id)
        if not doc_item: 
            abort(404)
        return doc_item

    @user_required
    def delete(self, doc_id):
        doc_item = DocModel.query_by_id(user, doc_id)
        if not doc_item:
            abort(404)
        doc_item.key.delete()
        return make_response("", 204)

    @marshal_with(doc_fields)
    @user_required
    def put(self, doc_id):
        doc_item = DocModel.query_by_id(user, doc_id)
        if not doc_item:
            abort(404)
        args = parser.parse_args()
        doc_item.populate(**args)
        doc_item.put()
        return doc_item

    @marshal_with(doc_fields)
    @user_required
    def post(self):
        args = parser.parse_args()
        doc_item.populate(**args)
        doc_item.put()
        return doc_item
