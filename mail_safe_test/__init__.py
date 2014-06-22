from authomatic import Authomatic
from flask import Flask
from mail_safe_test.oauth_keys import CONFIG
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

app.authomatic = Authomatic(config=CONFIG, secret=app.config.get('CSRF_SESSION_KEY'))

# Pull in URL dispatch routes
import urls
