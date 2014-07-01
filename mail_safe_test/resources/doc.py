from flask.ext import restful
from flask.ext.restful import fields, marshal_with, reqparse
from google.appengine.ext import ndb
from flask_ndb_api import NDBJSONEncoder
import json

class DocModel(ndb.Model):
    # id - in this key
    # owner - in parent key
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def query_by_owner(cls, owner):
        ancestor_key = ndb.Key("User", owner)
        return cls.query(ancestor=ancestor_key).order(-cls.date).get()

    @classmethod
    def query_by_id(cls, owner, doc_id):
        doc_key = ndb.Key("User", owner, DocModel, doc_id)
        return doc_key.get()

class DocList(restful.Resource):
    def get(self):
        # Validate owner.
        doc_list = DocModel.query_by_owner("owner")
        return json.dumps(doc_list, cls=NDBJSONEncoder)

class Doc(restful.Resource):
    def get(self, doc_id):
        # TODO: validate owner
        doc_item = DocModel.query_by_id("owner", doc_id)
        return json.dumps(doc_item, cls=NDBJSONEncoder)
        # TODO: return 401? when item is not found.

    def delete(self, todo_id):
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201
