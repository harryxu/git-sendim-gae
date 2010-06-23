import os

from google.appengine.api import xmpp
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util


class MainHandler(webapp.RequestHandler):
    def post(self):
        user_address = self.request.get('jid')
        user_msg = self.request.get('msg')

        if not xmpp.get_presence(user_address):
            xmpp.send_invite(user_address)
        else:
            status_code = xmpp.send_message(user_address, user_msg)
            self.response.out.write(status_code)

class InviteHandler(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'tpl/sendim/invite.html')
        self.response.out.write(template.render(path, {}))

    def post(self):
        email = self.request.get('email')
        xmpp.send_invite(email)

        path = os.path.join(os.path.dirname(__file__), 'tpl/sendim/invite.html')
        self.response.out.write(template.render(path, {
            'msg': 'Invation has been sent to %s.' % email
        }))

def main():
    application = webapp.WSGIApplication([
        ('/sendim', MainHandler),
        ('/sendim/invite', InviteHandler),
    ], debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
