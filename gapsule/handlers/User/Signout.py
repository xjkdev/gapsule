from gapsule.utils import authenticated
from gapsule.handlers.Base import BaseHandler


class SignOutHandler(BaseHandler):
    @authenticated
    def get(self):
        self.set_secure_cookie('session', '')
        self.redirect('/signin')
