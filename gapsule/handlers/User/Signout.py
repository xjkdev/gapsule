from gapsule.utils import authenticated
from gapsule.handlers.Base import BaseHandler
from gapsule.models.user import user_logout
from gapsule.utils.cookie_session import session_decode


class SignOutHandler(BaseHandler):
    @authenticated
    async def get(self):
        old_session = session_decode(
            self.get_secure_cookie('session')).get('session')
        await user_logout(self.current_user.user, old_session)
        self.set_secure_cookie('session', '')
        self.set_cookie('username', '')
        self.redirect('/signin')
