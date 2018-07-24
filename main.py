import webapp2
import os
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from models import Visitor

#remember, you can get this by searching for jinja2 google app engine
jinja_current_dir = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class SignInHandler(webapp2.RequestHandler):
    def get(self):
        me = users.get_current_user()
        if not me:
            start_template = jinja_current_dir.get_template("templates/welcome.html")
            jinja_values = {
                'signin_page_url': users.create_login_url('/')
            }

            self.response.write(start_template.render(jinja_values))
        else:
            my_key = ndb.Key('Visitor', me.user_id())
            my_visitor = my_key.get()
            if not my_visitor:
                my_visitor = Visitor(key = my_key, name = me.nickname(), email = me.email(),id = me.user_id(),
                page_view_count = 0)
            my_visitor.page_view_count += 1
            my_visitor.put()

            withuser_template = jinja_current_dir.get_template("templates/withuser.html")
            jinja_values = {
                'name': me.nickname(),
                'email_addr': me.email(),
                'user_id': me.user_id(),
                'signout_page_url': users.create_logout_url('/'),
                'number_of_views': my_visitor.page_view_count
            }

            self.response.write(withuser_template.render(jinja_values))


app = webapp2.WSGIApplication([
    ('/', SignInHandler),
], debug=True)
