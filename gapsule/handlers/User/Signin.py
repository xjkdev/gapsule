from tornado.escape import json_decode

from gapsule.handlers.Base import BaseHandler
from gapsule.utils import unauthenticated
from gapsule.utils.cookie_session import session_encode, format_log_time
from gapsule.utils.viewmodels import ViewModelDict, ViewModelField
from gapsule.models.user import verify_user


class SignInInput(ViewModelDict):
    username: str = ViewModelField(required=True)
    password: str = ViewModelField(required=True)


class SignInResult(ViewModelDict):
    state: str = ViewModelField(required=True)
    error: str = ViewModelField(required=False)


class SignInHandler(BaseHandler):
    @unauthenticated('/')
    def get(self):
        self.render('index.html')

    @unauthenticated('/')
    def post(self):
        data = SignInInput(json_decode(self.request.body))
        session = verify_user(data.username, data.password)
        logged_time = format_log_time()
        if session is not None:
            dataobj = dict(user=data.username, session=session,
                           logged_time=logged_time)
            self.set_secure_cookie(
                'session', session_encode(dataobj))
            self.set_cookie('username', data.username)
            self.write(SignInResult(state='ok'))
        else:
            self.write(SignInResult(state='error', error='validation failed.'))
