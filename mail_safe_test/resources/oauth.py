"""
oauth.py

"""

from flask import url_for, session, jsonify, abort, request
from flask_oauthlib.client import OAuthException
from mail_safe_test import app, google
from oauth2client.client import verify_id_token
from oauth2client.crypt import AppIdentityError

def login():
   print("login")
   return google.authorize(callback=url_for('authorized', _external=True))

def logout():
    session.clear()
    return("logged out", 200)

@google.authorized_handler
def oauth_callback(resp):
    """Basic OpenID connect profile. (Decorator makes a call to google)."""
    if isinstance(resp, OAuthException):
        return (resp.message, 502)
    if resp is None:
        return ('Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']), 403)
    #access_token = (resp['access_token'], '')
    id_token = resp['id_token']
    return jsonify({'id_token': id_token,
                    'verify_url': 'https://www.googleapis.com/oauth2/v1/tokeninfo?id_token=%s' % id_token})

def verify():
    id_token = request.headers.get('Authorization')
    if not id_token:
        abort(400)
    try:
        jwt = verify_id_token(id_token, app.config.get('GOOGLE_ID'))
        return jsonify(jwt)
    except AppIdentityError as e:
        print "error", e
        abort(403)

