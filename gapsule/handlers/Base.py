from typing import Union
from tornado import web, escape
from gapsule.utils.cookie_session import session_decode
from gapsule.models.user import check_session_status


class AuthState():
    __slots__ = ['user', 'active']

    def __init__(self, user, active=False):
        self.user = user
        self.active = active


class BaseHandler(web.RequestHandler):

    async def prepare(self):
        data = self.get_secure_cookie('session')
        if data is None:
            return None
        try:
            dataobj = session_decode(data)
            user = dataobj.get('user', None)
            session = dataobj.get('session', None)
            logged_time = dataobj.get('logged_time', None)
            if await check_session_status(user, session):
                self.current_user = AuthState(user, True)
            elif user is not None:
                self.current_user = AuthState(user, False)
            else:
                self.current_user = None
        except Exception as e:
            print(e)
            self.current_user = None

    def get_login_url(self):
        self.require_setting(
            "verify_url", "@gapsule.utils.authenticated")
        return self.application.settings["verify_url"]

    def get_verify_url(self):
        self.require_setting(
            "verify_url", "@gapsule.utils.active_authenticated")
        return self.application.settings["verify_url"]

    def get_template_name(self):
        return 'index.html'

    def write(self, chunk: Union[str, bytes, dict]) -> None:
        """Writes the given chunk to the output buffer.

        To write the output to the network, use the `flush()` method below.

        If the given chunk is a dictionary or list, we write it as JSON and set
        the Content-Type of the response to be ``application/json``.
        (if you want to send JSON as a different ``Content-Type``, call
        ``set_header`` *after* calling ``write()``).

        Note that lists are not converted to JSON because of a potential
        cross-site security vulnerability.  All JSON output should be
        wrapped in a dictionary.  More details at
        http://haacked.com/archive/2009/06/25/json-hijacking.aspx/ and
        https://github.com/facebook/tornado/issues/1009
        """
        if isinstance(chunk, list):
            chunk = escape.json_encode(chunk)
            self.set_header("Content-Type", "application/json; charset=UTF-8")
        super().write(chunk)
