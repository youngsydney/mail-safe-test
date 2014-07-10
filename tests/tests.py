#!/usr/bin/env python
# encoding: utf-8
"""
tests.py

"""
import os
import json
import unittest
from google.appengine.ext import testbed
from mail_safe_test import app

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
    

class NonAuthUserTestCases(unittest.TestCase):

    def setUp(self):
        common_setUp(self)

    def tearDown(self):
        self.testbed.deactivate()
        
    def test_user_endpoint(self):
        rv = self.app.get('/user/')
        assert rv.status_code == 400    

    def test_user_id_endpoint(self):
        rv = self.app.get('/user/1/')
        assert rv.status_code == 404
        
    def test_create_valid_user(self):
        response = self.app.post('/user/',
            data='{"first_name": "Testy", "last_name": "McTest", "email": "test@example.com"}',
            content_type='application/json',            
            headers = dict(Authorization = '1'))        
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['first_name'] == 'Testy'
        assert data['last_name'] == 'McTest'
        assert data['email'] == 'test@example.com'
        #TODO (hpshelton 7/9/14): Verify the created date/time and the uri
        
    def test_create_invalid_user(self):
        response = self.app.post('/user/',
            data='{"first_name": "Testy", "last_name": "McTest"}',
            content_type='application/json',            
            headers = dict(Authorization = '1'))        
        assert response.status_code == 400

        data = json.loads(response.data)
        assert data['message'] == 'Missing required parameter email in json' # Maybe check non-null or non-empty here?


class UserAuthUserTestCases(unittest.TestCase):
    
    def setUp(self):
        common_setUp(self)

        # Provision a valid user
        response = self.app.post('/user/',
            data='{"first_name": "Testy", "last_name": "McTest", "email": "test@example.com"}',
            content_type='application/json',            
            headers = dict(Authorization = '1'))      
        assert response.status_code == 200

        # Store the generated user id in a static variable
        # TODO (hpshelton 7/9/14) Is this always equal to 1?
        data = json.loads(response.data)
        UserAuthUserTestCases.user_id = data['uri'].split('/')[-2]

    def tearDown(self):
        self.testbed.deactivate()

    def test_user_endpoint(self):        
        rv = self.app.get('/user/', headers = dict(Authorization = UserAuthUserTestCases.user_id))
        assert rv.status_code == 200

    # TODO (hpshelton 7/9/14): This seems like a bug; /user/ and /user/id/ should probably be equivalent with appropriate auth
    def test_user_id_endpoint(self):
        rv = self.app.get('/user/' + UserAuthUserTestCases.user_id + '/', headers = dict(Authorization = UserAuthUserTestCases.user_id))
        assert rv.status_code == 404

# TODO (hpshelton 7/9/14): This probably can't be tested until I can programmatically generate admin users (or we build a default admin id test hook)
class AdminAuthUserTestCases(unittest.TestCase):

    def setUp(self):
        common_setUp(self)

        # Provision a valid admin user
        # TODO

        # Store the generated admin user id in a static variable
        AdminAuthUserTestCases.admin_id = 1
    def tearDown(self):
        self.testbed.deactivate()
        
'''
    def test_users_endpoint(self):
        rv = self.app.get('/admin/users/', headers = dict(Authorization = AdminAuthUserTestCases.admin_id))
        assert rv.status_code == 200

        data = json.loads(response.data)
        assert data['users'][0]['first_name'] == 'Admin'
        assert data['users'][0]['last_name'] == 'McAdmin'
        assert data['users'][0]['email'] == 'admin@example.com'
'''  
