#!/usr/bin/env python
# encoding: utf-8
"""
tests.py

"""
from google.appengine.ext import testbed
from mail_safe_test import app
from unittest import TestCase

class UserApiTests(TestCase):
    def setUp(self):
        # Flask apps testing. See: http://flask.pocoo.org/docs/testing/
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        self.app = app.test_client()
        # Setups app engine test bed. See: http://code.google.com/appengine/docs/python/tools/localunittesting.html#Introducing_the_Python_Testing_Utilities
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_user_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_create_user(self):
        rv = self.app.post('/user/', data={}, content_type="application/json", headers=[("Authorization", "1")])
        self.assertEqual('200 OK',  rv.status)

    def test_users(self):
        rv = self.app.get('/user/')
        self.assertEqual('200 OK',  rv.status)

'''
    def test_no_user(self):
        rv = self.app.get('/user/1/')
        assert rv.status == '200 OK'

    def test_contacts(self):
        rv = self.app.get('/user/1/contact/')
        assert rv.status == '200 OK'

    def test_no_contact(self):
        rv = self.app.get('/user/1/contact/1/')
        assert rv.status == '200 OK'

    def test_docs(self):
        rv = self.app.get('/user/1/doc/')
        assert rv.status == '200 OK'

    def test_no_doc(self):
        rv = self.app.get('/user/1/doc/1/')
        assert rv.status == '200 OK'

    def test_link(self):
        rv = self.app.get('/link/1/')
        assert rv.status == '200 OK'
        '''
