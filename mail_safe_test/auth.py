"""
auth.py

Common code for retreiving and validating the user from the
Authorization header.
"""

from flask import request, abort
from functools import wraps
from google.appengine.ext import ndb

class UserModel(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()
    admin = ndb.BooleanProperty(default=False)
    created = ndb.DateTimeProperty(auto_now_add=True)
    last_active = ndb.DateTimeProperty(auto_now_add=True)

def current_user(request):
    '''Returns None if the user is not found.'''
    id_token = request.headers.get('Authorization')
    if not id_token:
        abort(400)
    # TODO(gdbelvin): Verify id token.
    # TODO(gdbelvin): Extract `sub`, the unique_key.
    sub = id_token
    return ndb.Key(UserModel, sub).get()

def user_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_user = current_user(request)
        if not auth_user:
            abort(403)
        return func(*args, **kwargs)
    return wrapper

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_user = current_user(request)
        if not auth_user or not auth_user.admin:
            abort(403)
        return func(*args, **kwargs)
    return wrapper

