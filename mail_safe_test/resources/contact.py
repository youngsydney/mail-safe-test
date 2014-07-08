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

#	Class NDBUrl? is this something that needs to be in every .py?

# Public exports
contact_fields = {
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'phone': fields.String,
    'uri': NDBUrl('/user/contact/')
#	'uri': NDBUrl('/user/contacts/')
}

parser = reqparse.RequestParser()
parser.add_argument('first_name', type = str, location = 'json')
parser.add_argument('last_name', type = str, location = 'json')
parser.add_argument('email', type = str, location = 'json')
parser.add_argument('phone', type = str, location = 'json')
parser.add_argument('Authorization', type=str, required=True, location='headers',
                            dest='oauth')

class ContactModel(ndb.Model):
    # id - in this key
    # owner - in parent key (author/user)
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()
    phone = ndb.StringProperty()
    oauth = ndb.StringProperty()

    @classmethod
    def query_by_owner(cls, owner):
        ancestor_key = ndb.Key("User", owner)
        return cls.query(ancestor=ancestor_key).order(-cls.date).get()

    @classmethod
    def query_by_id(cls, owner, contact_id):
        contact_key = ndb.Key("User", owner, ContactModel, contact_id)
        return contact_key.get()

def get_owner(request):
    owner_id = request.headers.get('Authorization')
    if not owner_id or not owner_id.isdigit():
        abort(400)
    key_id = int(owner_id)
    return ndb.Key(UserModel, owner_id).get()

class ContactListAPI(restful.Resource):
    contact_list_fields = {'contacts': fields.List(fields.Nested(contact_fields))}
    
    @marshal_with(contact_list_fields)
    def get(self):
    	owner = get_owner(request)
        if not auth_owner
            abort(403)
    	contacts = ContactModel.query_by_owner("owner")
    	return {'contacts': contacts}

    @marshal_with(contact_list_fields)
    def delete(self):
    	ndb.delete_multi(ContactModel.query_by_owner("owner")
    	contacts = ContactModel.query_by_owner("owner")
    	return {'contacts': contacts}

class ContactAPI(restful.Resource):
    def __init__(self):
        self.post_parser = parser.copy()
        self.post_parser.replace_argument('email', type = str, required = True, location = 'json')
        self.put_parser = parser.copy()
        super(ContactAPI, self).__init__()

    @marshal_with(contact_fields)
    def get(self, contact_id):
        owner = get_owner(request)
        if not auth_owner
            abort(403)
        contact = ContactModel.query_by_id("owner", contact_id)
        if contact is None:
            abort(404)
        return contact

    @marshal_with(contact_fields)
    def post(self, contact_id):
        owner = get_owner(request)
        if not auth_owner
            abort(403)
        contact = ContactModel.query_by_id("owner", contact_id)
        if contact is not None:
            abort(403)
        args = self.post_parser.parse_args()
        contact = ContactModel(**args)
        contact.put()
        return contact

    @marshal_with(contact_fields)
    def put(self, contact_id):
        owner = get_owner(request)
        if not auth_owner
            abort(403)
        contact = ContactModel.query_by_id("owner", contact_id)
        if not contact:
            abort(404)
        args = self.put_parser.parse_args()
        contact.populate(**args)
        contact.put()
        return contact

    def delete(self, contact_id):
        owner = get_owner(request)
        if not auth_owner
            abort(403)
        contact = ContactModel.query_by_id("owner", contact_id)
        if not contact:
            abort(404)
        contact.key.delete()
        return make_response("", 204)
