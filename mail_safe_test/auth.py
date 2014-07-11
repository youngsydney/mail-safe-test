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
    oauth = ndb.StringProperty()
    admin = ndb.BooleanProperty(default=False)
    created = ndb.DateTimeProperty(auto_now_add=True)
    last_active = ndb.DateTimeProperty(auto_now_add=True)

def current_user(request):
    '''Returns None if the user is not found.'''
    # TODO(gdb): Verify authorization header with oauth.
    user_id = request.headers.get('Authorization')
    if not user_id or not user_id.isdigit():
        abort(400)
    key_id = int(user_id)
    return ndb.Key(UserModel, key_id).get()

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

