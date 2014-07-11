"""
oauth.py

"""

from flask import url_for, session, jsonify
from flask_oauthlib.client import OAuthException
from mail_safe_test import app, google

def login():
   print("login")
   return google.authorize(callback=url_for('authorized', _external=True))

def logout():
    session.clear()
    return("logged out", 200)

# Basic OpenID connect profile. (This decorator makes a call to google)
# TODO(gdbelvin): implement implicit profile (no extra call)
@google.authorized_handler
def oauth_callback(resp):
    if isinstance(resp, OAuthException):
        return (resp.message, 502)
    if resp is None:
        return ('Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']), 403)
    session['google_token'] = (resp['access_token'], '')
    # TODO: validate ID token in implicit mode
    # TODO: remove dependence on cookies.
    me = google.get('userinfo')
    return jsonify({"data": me.data})

@google.tokengetter
def get_github_oauth_token():
    return session.get('google_token')

