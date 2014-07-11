#!/usr/bin/env python
# encoding: utf-8
"""
tests.py

"""

from json import loads
from google.appengine.ext import testbed
from mail_safe_test import app
from unittest import TestCase

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

class NonAuthUserTestCases(TestCase):

    def setUp(self):
        common_setUp(self)
        self.data='{"first_name": "Testy", "last_name": "McTest", "email": "test@example.com"}'

    def tearDown(self):
        self.testbed.deactivate()

    def test_user_endpoint(self):
        rv = self.app.get('/user/')
        self.assertEqual(400, rv.status_code)

    def test_user_id_endpoint(self):
        rv = self.app.get('/user/1/')
        self.assertEqual(404, rv.status_code)

    def test_create_valid_user(self):
        rv = self.app.post('/user/',
                data=self.data,
                content_type='application/json',
                headers = {'Authorization': '1'})
        self.assertEqual(200, rv.status_code)

        data = loads(rv.data)
        self.assertEqual('Testy', data['first_name'])
        self.assertEqual('McTest', data['last_name'])
        self.assertEqual('test@example.com', data['email'])
        #TODO (hpshelton 7/9/14): Verify the created date/time and the uri

    def test_create_invalid_user(self):
        rv = self.app.post('/user/',
            data='{"first_name": "Testy", "last_name": "McTest"}',
            content_type='application/json',
            headers = {'Authorization': '1'})
        self.assertEqual(400, rv.status_code)

        data = loads(rv.data)
        # Maybe check non-null or non-empty here?
        self.assertEqual('Missing required parameter email in json',
                         data['message'])

    def test_put_invalid_user(self):
        rv = self.app.post('/user/',
            data='{"first_name": "Testy", "last_name": "McTest"}',
            content_type='application/json',
            headers = {'Authorization': '100'})
        self.assertEqual(400, rv.status_code)

class UserAuthUserTestCases(TestCase):

    def setUp(self):
        common_setUp(self)

        # Provision a valid user
        UserAuthUserTestCases.user_id = '1'
        rv = self.app.post('/user/',
            data='{"first_name": "Testy", "last_name": "McTest", "email": "test@example.com"}',
            content_type='application/json',
            headers = {'Authorization': UserAuthUserTestCases.user_id})
        self.assertEqual(200, rv.status_code)

    def tearDown(self):
        self.testbed.deactivate()

    def test_user_endpoint(self):
        rv = self.app.get('/user/',
            headers = {'Authorization': UserAuthUserTestCases.user_id})
        self.assertEqual(200, rv.status_code)

    def test_user_put(self):
        rv = self.app.put('/user/',
            data='{"first_name": "Changed"}',
            content_type='application/json',
            headers = {'Authorization': UserAuthUserTestCases.user_id})
        self.assertEqual(200, rv.status_code)

    def test_user_delete(self):
        rv = self.app.delete('/user/',
            headers = {'Authorization': UserAuthUserTestCases.user_id})
        self.assertEqual(204, rv.status_code)

class AdminAuthUserTestCases(TestCase):

    def setUp(self):
        common_setUp(self)

        # Provision a valid admin user
        AdminAuthUserTestCases.admin_id = "0" #Ids are strings

        from mail_safe_test.auth import UserModel
        from google.appengine.ext import ndb
        args = {"id": AdminAuthUserTestCases.admin_id,
                "first_name": "Admin",
                "last_name": "McAdmin",
                "email": "admin@example.com",
                "admin": True}
        user = UserModel(**args)
        user.put()

    def tearDown(self):
        self.testbed.deactivate()

    def test_users_endpoint(self):
        rv = self.app.get('/admin/users/',
            headers = {'Authorization': AdminAuthUserTestCases.admin_id})
        self.assertEqual(200, rv.status_code)

        data = loads(rv.data)
        self.assertEqual('Admin', data['users'][0]['first_name'])
        self.assertEqual('McAdmin', data['users'][0]['last_name'])
        self.assertEqual('admin@example.com', data['users'][0]['email'])
