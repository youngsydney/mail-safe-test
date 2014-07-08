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
from mail_safe_test import user

#   Class NDBUrl? is this something that needs to be in every .py?

#   public exports
doc_fields = {
    'content': fields.String,
    'date': fields.DateTime,
    'status': fields.String,
    'uri': NDBUrl('/user/doc/')
#   'uri': NDBUrl('/user/docs/')
}

parser = reqparse.RequestParser()
parser.add_argument('content', type = str, location = 'json')
parser.add_argument('status', type = str, location = 'json')
parser.add_argument('Authorization', type=str, required=True, location='headers',
                            dest='oauth')

class DocModel(ndb.Model):
    # id - in this key
    # owner - in parent key (user)
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    status = ndb.StringProperty()
    oauth = ndb.StringProperty()

    @classmethod
    def query_by_owner(cls, owner):
        ancestor_key = ndb.Key("User", owner)
        return cls.query(ancestor=ancestor_key).order(-cls.date).get()

    @classmethod
    def query_by_id(cls, owner, doc_id):
        doc_key = ndb.Key("User", owner, DocModel, doc_id)
        return doc_key.get()

def get_owner(request):
    owner_id = request.headers.get('Authorization')
    if not owner_id or not owner_id.isdigit():
        abort(400)
    key_id = int(owner_id)
    return ndb.Key(UserModel, owner_id).get()

class DocListAPI(restful.Resource):
    doc_list_fields = {'users': fields.List(fields.Nested(doc_fields))}

    def get(self):
        owner = get_owner(request)
        if not auth_owner
            abort(403)
        doc_list = DocModel.query_by_owner("owner")
        return json.dumps(doc_list, cls=NDBJSONEncoder)

    @marshal_with(doc_list_fields)
    def delete(self):
        ndb.delete_multi(DocModel.query_by_owner("owner")
        docs = DocModel.query_by_owner("owner")
        return {'docs': docs}

class DocAPI(restful.Resource):
    def __init__(self):
        self.post_parser = parser.copy()
        self.post_parser.replace_argument('owner', type = str, required = True, location = 'json')
        self.put_parser = parser.copy()
        super(DocAPI, self).__init__()

    def get(self, doc_id):
        owner = get_owner(request)
        if not auth_owner
            abort(403)
        doc_item = DocModel.query_by_id("owner", doc_id)
        if doc_item is None
            abort(404)
        return json.dumps(doc_item, cls=NDBJSONEncoder)

    def delete(self, doc_id):
        owner = get_owner(request)
        if not auth_owner
            abort(403)
        doc_item = DocModel.query_by_id("owner", doc_id)
        if doc_item is None
            abort(404)
        doc_item.key.delete()
        return "", 204

    def put(self, doc_id):
        owner = get_owner(request)
        if not auth_owner
            abort(403)
        doc_item = DocModel.query_by_id("owner", doc_id)
        if doc_item is None
            abort(404)
        args = parser.parse_args()
        doc_item.populate(**args)
        doc_item.put()
        return doc_item, 201

    def post(self, doc_id):
        owner = get_owner(request)
        if not auth_owner
            abort(403)
        doc_item = DocModel.query_by_id("owner", doc_id)
        if doc_item is not None
            abort(403)
        args = parser.parse_args()
        doc_item.populate(**args)
        doc_item.put()
        return doc_item, 201
