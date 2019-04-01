import json
import base64
import datetime

from gapsule.handlers.Base import BaseHandler
from gapsule.utils import unauthenticated
from gapsule.models.user import verify_user


class SignInHandler(BaseHandler):
    @unauthenticated('/')
    def get(self):
        self.render('index.html')

    @unauthenticated('/')
    def post(self):
        username = self.get_body_argument('username')
        password = self.get_body_argument('password')
        session = verify_user(username, password)
        logged_time = datetime.datetime.now().strftime("%Y/%m/%d% %H:%M:%S")
        if session is not None and username is not None and password is not None:
            dataobj = dict(user=username, session=session,
                           logged_time=logged_time)
            self.set_secure_cookie(
                'session', base64.encodestring(json.dumps(dataobj)))
            self.write(dict(state='ok.'))
        else:
            self.write(dict(error='validation failed.'))
