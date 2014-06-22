"""
urls.py

URL dispatch route mappings and error handlers

"""
from mail_safe_test import app
from mail_safe_test import views
from mail_safe_test import resources
from mail_safe_test.resources.user import Users, User
from mail_safe_test.resources.contact import Contacts, Contact
from mail_safe_test.resources.doc import Docs, Doc
from mail_safe_test.resources.link import Link

from flask.ext import restful

api = restful.Api(app)

app.add_url_rule('/login/<provider_name>/', view_func=views.login, methods=['GET', 'POST'])

# Login required
#api.add_resource(Users,    '/user/')
#api.add_resource(User,     '/user/<int:user_id>/')
api.add_resource(Contacts, '/contact/')
api.add_resource(Contact,  '/contact/<int:contact_id>/')
#api.add_resource(Docs,     '/doc')
#api.add_resource(Doc,      '/doc/<int:doc_id>')

# Login not required
#api.add_resource(Link,     '/link/<int:link_id>')

## Error handlers
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return "Page not found", 404
# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return "500 Error", 500
