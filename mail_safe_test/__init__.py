from flask import Flask
from flask_oauthlib.client import OAuth
import os

app = Flask('mail_safe_test')

def is_development():
    return os.getenv('SERVER_SOFTWARE') and (
        os.getenv('SERVER_SOFTWARE').startswith('Development'))

if os.getenv('FLASK_CONF') == 'TEST':
    app.config.from_object('mail_safe_test.settings.Testing')
elif is_development():
    app.config.from_object('mail_safe_test.settings.Development')
else:
    app.config.from_object('mail_safe_test.settings.Production')

oauth = OAuth(app)
google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'https://www.googleapis.com/auth/userinfo.email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

# Pull in URL dispatch routes
import urls
