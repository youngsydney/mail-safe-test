#auth.py
# Common code for retreiving and validating the user from the
# Authorization header.

from functools import wraps
from google.appengine.ext import ndb

def get_user(request):
    # TODO(gdb): Verify authorization header loop up user.
    user_id = request.headers.get('Authorization')
    if not user_id or not user_id.isdigit():
        abort(400)
    key_id = int(user_id)
    return ndb.Key(UserModel, key_id).get()

def user_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_user = get_user(request)
        print "authuser", auth_user
        if not auth_user:
            abort(403)
        kwargs['auth_user'] = auth_user
        return func(*args, **kwargs)
    return wrapper

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_user = get_user(request)
        if not auth_user or not auth_user.admin:
            abort(403)
        kwargs['auth_user'] = auth_user
        return func(*args, **kwargs)
    return wrapper

