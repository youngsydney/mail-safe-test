#!/usr/bin/env python
# encoding: utf-8
"""
tests.py

"""

from google.appengine.ext import ndb
from google.appengine.ext import testbed
from json import loads
from unittest import TestCase
from mail_safe_test import app
from mail_safe_test.auth import UserModel
from mail_safe_test.resources.contact import ContactList, Contact, ContactModel

def common_setUp(self):
    # Flask apps testing. See: http://flask.pocoo.org/docs/testing/
    app.config['TESTING'] = True
    app.config['CSRF_ENABLED'] = False
    self.app = app.test_client()
    # Setup app engine test bed. See: http://code.google.com/appengine/docs/python/tools/localunittesting.html#Introducing_the_Python_Testing_Utilities
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_datastore_v3_stub()
    self.testbed.init_user_stub()
    self.testbed.init_memcache_stub()

class AuthUserContactTestCases(TestCase):

    def setUp(self):
        common_setUp(self)

        AuthUserContactTestCases.user_id = '111111111111111111111'
        AuthUserContactTestCases.user_token = "valid_user"

        # Provision a valid user
        args = {"id": AuthUserContactTestCases.user_id,
                "first_name": "Testy",
                "last_name": "McTest",
                "email": "test@example.com" }
        user = UserModel(**args)
        user.put()

    def tearDown(self):
    	self.testbed.deactivate()

    def test_contact_put(self):
        args = {"email" : "bestfriend@example.com"}
        contact = ContactModel(**args)
        contact.put()

    def test_contact_post(self):
        AuthUserContactTestCases.contact_id = "25"

        args = {"id" : AuthUserContactTestCases.contact_id,
                "first_name" : "Best",
                "last_name" : "Friend",
                "email" : "friend@example.com",
                "phone" : "123456789001"}
        contact = ContactModel(**args)
        contact.put()





