"""
auth.py

Common code for retreiving and validating the user from the
Authorization header.
"""

from flask import request, abort, redirect, url_for
from functools import wraps
from google.appengine.ext import ndb
from mail_safe_test import app
from oauth2client.client import verify_id_token
from oauth2client.crypt import AppIdentityError

class UserModel(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()
    admin = ndb.BooleanProperty(default=False)
    created = ndb.DateTimeProperty(auto_now_add=True)
    last_active = ndb.DateTimeProperty(auto_now_add=True)

def current_user():
    """Returns None if the user is not found."""
    jwt = current_user_token_info()
    if not jwt:
        return None
    user_id = jwt['sub']
    return ndb.Key(UserModel, user_id).get()

def current_user_token_info():
    """Returns the user info object if a valid id_token is in the Authorization header."""
    id_token = request.headers.get('Authorization')
    if not id_token:
        return None
    if app.config['TESTING'] and id_token == "valid_user":
        return {
            "at_hash": "x_UrBCcmyP2xSki42gqOxw",
            "aud": app.config.get('GOOGLE_ID'),
            "azp": app.config.get('GOOGLE_ID'),
            "cid": app.config.get('GOOGLE_ID'),
            "email": "user@example.com",
            "email_verified": True,
            "exp": 1405154845,
            "iat": 1405150945,
            "id": "111111111111111111111",
            "iss": "accounts.google.com",
            "sub": "111111111111111111111",
            "token_hash": "xxxxxxxxxxxxxxxxxxxxxx",
            "verified_email": True
        }
    elif app.config['TESTING'] and id_token == "valid_user2":
        return {
            "at_hash": "x_UrBCcmyP2xSki42gqOxw",
            "aud": app.config.get('GOOGLE_ID'),
            "azp": app.config.get('GOOGLE_ID'),
            "cid": app.config.get('GOOGLE_ID'),
            "email": "user2@example.com",
            "email_verified": True,
            "exp": 1405154845,
            "iat": 1405150945,
            "id": "111111111111111111112",
            "iss": "accounts.google.com",
            "sub": "111111111111111111112",
            "token_hash": "xxxxxxxxxxxxxxxxxxxxxx",
            "verified_email": True
        }
    elif app.config['TESTING'] and id_token == "valid_admin":
        return {
            "at_hash": "x_UrBCcmyP2xSki42gqOxw",
            "aud": app.config.get('GOOGLE_ID'),
            "azp": app.config.get('GOOGLE_ID'),
            "cid": app.config.get('GOOGLE_ID'),
            "email": "admin@example.com",
            "email_verified": True,
            "exp": 1405154845,
            "iat": 1405150945,
            "id": "222222222222222222222",
            "iss": "accounts.google.com",
            "sub": "222222222222222222222",
            "token_hash": "xxxxxxxxxxxxxxxxxxxxxx",
            "verified_email": True
        }
    elif app.config['TESTING'] and id_token == "valid_user_contact":
        return {
            "at_hash": "x_UrBCcmyP2xSki42gqOxw",
            "aud": app.config.get('GOOGLE_ID'),
            "azp": app.config.get('GOOGLE_ID'),
            "cid": app.config.get('GOOGLE_ID'),
            "email": "usercontact@example.com",
            "email_verified": True,
            "exp": 1405154845,
            "iat": 1405150945,
            "id": "111111111111111111112",
            "iss": "accounts.google.com",
            "sub": "111111111111111111112",
            "token_hash": "xxxxxxxxxxxxxxxxxxxxxx",
            "verified_email": True
        }
    try:
        return verify_id_token(id_token, app.config.get('GOOGLE_ID'))
        user_id = jwt['sub']
        return ndb.Key(UserModel, user_id).get()
    except AppIdentityError as e:
        if not (app.config['TESTING'] and id_token == "invalid"):
            print "error", e
        return None

def user_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_user = current_user()
        if not auth_user:
            abort(403)
        return func(*args, **kwargs)
    return wrapper

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_user = current_user()
        if not auth_user or not auth_user.admin:
            abort(403)
        return func(*args, **kwargs)
    return wrapper

