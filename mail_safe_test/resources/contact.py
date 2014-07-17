"""
contact.py

"""

from flask import request, Response, abort, make_response
from flask.ext.restful import Resource, fields, marshal_with, reqparse
from google.appengine.ext import ndb
from mail_safe_test.custom_fields import NDBUrl
from mail_safe_test.auth import current_user, user_required, admin_required, UserModel

# Public exports
contact_fields = {
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'phone': fields.String,
    'uri': NDBUrl('/user/contact/')
}

parser = reqparse.RequestParser()
parser.add_argument('first_name', type = str, location = 'json')
parser.add_argument('last_name', type = str, location = 'json')
parser.add_argument('email', type = str, location = 'json')
parser.add_argument('phone', type = str, location = 'json')

class ContactModel(ndb.Model):
    # id - in this key
    # user - in parent key (author/user)
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()
    phone = ndb.StringProperty()
    oauth = ndb.StringProperty()

    @classmethod
    def query_by_id(cls, user, contact_id):
        contact_key = ndb.Key(UserModel, user, ContactModel, contact_id)
        return contact_key.get()

class ContactList(Resource):
    method_decorators = [user_required]
    contact_list_fields = {'contacts': fields.List(fields.Nested(contact_fields))}
    
    @marshal_with(contact_list_fields)
    @user_required
    def get(self):
    	contacts = ContactModel.query().fetch()
    	return {'contacts': contacts}

    @marshal_with(contact_list_fields)
    @user_required
    def delete(self):
    	ndb.delete_multi(ContactModel.query().fetch(keys_only=True))
        contacts = ContactModel.query().fetch()
        return {'contacts': contacts}

class Contact(Resource):
    def __init__(self):
        self.post_parser = parser.copy()
        self.post_parser.replace_argument('email', type = str, required = True, location = 'json')
        self.put_parser = parser.copy()
        super(ContactAPI, self).__init__()

    @marshal_with(contact_fields)
    @user_required
    def get(self, contact_id):
        contact = ContactModel.query_by_id(user, contact_id)
        if contact is None:
            abort(404)
        return contact

    @marshal_with(contact_fields)
    @user_required
    def post(self):
        # Define required POST params
        if self.post_parser is None:
            self.post_parser = parser.copy()
            self.post_parser.replace_argument('email', type = str, required = True, location = 'json')
            self.post_parser.replace_argument('phone', type = str, required = True, location = 'json')
        jwt = current_user_token_info()
        if not jwt:
            abort(400)
        args['id'] = jwt['sub']
        args = self.post_parser.parse_args()
        contact = ContactModel(**args)
        contact.put()
        return contact

    @marshal_with(contact_fields)
    @user_required
    def put(self, contact_id):
        contact = ContactModel.query_by_id(user, contact_id)
        if not contact:
            abort(404)
        args = self.put_parser.parse_args()
        contact.populate(**args)
        contact.put()
        return contact

    @user_required
    def delete(self, contact_id):
        contact = ContactModel.query_by_id(user, contact_id)
        if not contact:
            abort(404)
        contact.key.delete()
        return make_response("", 204)
