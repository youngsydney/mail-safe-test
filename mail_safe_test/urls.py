"""
urls.py

URL dispatch route mappings

"""
from mail_safe_test import app
from mail_safe_test import resources
from mail_safe_test.resources.user import UserAPI, AdminUserAPI, AdminUserListAPI
from mail_safe_test.resources.contact import ContactList, Contact
from mail_safe_test.resources.doc import DocList, Doc
from mail_safe_test.resources.link import Link
from mail_safe_test.errors import HTTP_Error

from flask.ext import restful

app.api = restful.Api(app)

app.api.add_resource(AdminUserAPI, '/admin/user/<int:key_id>/', endpoint = '/admin/user/')
app.api.add_resource(AdminUserListAPI, '/admin/users/', endpoint = '/admin/users/')

# Resources for the currently logged in user
app.api.add_resource(UserAPI, '/user/', endpoint = '/user/')
#app.api.add_resource(Contact,  '/user/contact/<int:contact_id>/',endpoint =  '/contact/')
app.api.add_resource(Doc,       '/user/doc/<int:doc_id>/', endpoint = '/doc/')

# Login not required
#app.api.add_resource(Link,     '/link/<int:link_id>/')
