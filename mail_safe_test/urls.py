"""
urls.py

URL dispatch route mappings

"""
from mail_safe_test import app
from mail_safe_test import resources
from mail_safe_test.resources.user import UserAPI
from mail_safe_test.resources.contact import ContactList, Contact
from mail_safe_test.resources.doc import DocList, Doc
from mail_safe_test.resources.link import Link
from mail_safe_test.errors import HTTP_Error

from flask.ext import restful

app.api = restful.Api(app)
api = app.api

# Login required
api.add_resource(UserAPI,    '/user/')
#api.add_resource(Contact,  '/contact/<int:contact_id>/')
api.add_resource(Doc,      '/doc/<int:doc_id>')

# Login not required
#api.add_resource(Link,     '/link/<int:link_id>')
