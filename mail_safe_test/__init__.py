from flask import Flask
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


# Pull in URL dispatch routes
import urls
