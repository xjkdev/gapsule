from tornado import web
import json
import base64
from gapsule.models.user import check_session_status


class AuthState():
    __slots__ = ['user', 'active']

    def __init__(self, user, active=False):
        self.user = user
        self.active = active


class BaseHandler(web.RequestHandler):

    def get_current_user(self):
        data = self.get_secure_cookie('session')
        if data is None:
            return None
        try:
            dataobj = json.loads(base64.decodebytes(data))
            user = dataobj.get('user', None)
            session = dataobj.get('session', None)
            logged_time = dataobj.get('logged_time', None)
            if check_session_status(user, session, logged_time):
                return AuthState(user, True)
            elif user is not None:
                return AuthState(user, False)
            else:
                return None
        except Exception as e:
            print(e)
            return None

    def get_login_url(self):
        self.require_setting(
            "verify_url", "@gapsule.utils.authenticated")
        return self.application.settings["verify_url"]

    def get_verify_url(self):
        self.require_setting(
            "verify_url", "@gapsule.utils.active_authenticated")
        return self.application.settings["verify_url"]
