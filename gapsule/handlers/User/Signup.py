from tornado.escape import json_decode
from tornado.web import HTTPError
from gapsule.handlers.Base import BaseHandler
from gapsule.utils import unauthenticated, ajaxquery
from gapsule.utils.viewmodels import ViewModelDict, ViewModelField
from gapsule.models.user import add_user_pending_verifying, create_new_user, set_profile
from gapsule.models.signup_token import check_token, get_pending_email, remove_token


class SignUpInputStep1(ViewModelDict):
    username = ViewModelField(required=True, nullable=False)
    password = ViewModelField(required=True, nullable=False)
    email = ViewModelField(required=True, nullable=False)


class SignUpInputStep2(ViewModelDict):
    username = ViewModelField(required=True, nullable=False)
    password = ViewModelField(required=True, nullable=False)
    token = ViewModelField(required=True, nullable=False)


class SignUpInputStep3(ViewModelDict):
    username = ViewModelField(required=True, nullable=False)
    password = ViewModelField(required=True, nullable=False)
    token = ViewModelField(required=True, nullable=False)
    icon = ViewModelField(required=False)
    firstname = ViewModelField(required=True, nullable=False)
    secondname = ViewModelField(required=True, nullable=False)
    biography = ViewModelField(required=False)
    company = ViewModelField(required=False)
    location = ViewModelField(required=False)
    website = ViewModelField(required=False)


class SignUpResult(ViewModelDict):
    state = ViewModelField(required=True, nullable=False)
    error = ViewModelField(required=False)
    token = ViewModelField(required=False, nullable=True)


class SignUpHandler(BaseHandler):
    @unauthenticated('/')
    def get(self, action=None):
        self.render('index.html')

    @unauthenticated('/')
    async def post(self, action=None):
        if action is None:  # Step 1
            try:
                data = SignUpInputStep1(json_decode(self.request.body))
                token = add_user_pending_verifying(
                    data.username, data.email, data.password)
                self.write(SignUpResult(state='ok', token=token))
            except Exception as e:  # TODO: check exceptions.
                self.write(SignUpResult(state='error',
                                        error=str(e)))
        elif action == '/verify':
            try:
                data = SignUpInputStep2(json_decode(self.request.body))
                if check_token(data.username, data.password, data.token):
                    self.write(SignUpResult(state='ok'))
                else:
                    self.write(SignUpResult(
                        state='error', error='token or password error'))
            except:  # TODO: check exceptions.
                self.write(SignUpResult(state='error',
                                        error='invalid token, username or password.'))
        elif action == '/finishing':
            try:
                data = SignUpInputStep3(json_decode(self.request.body))
                if check_token(data.username, data.password, data.token):
                    email = get_pending_email(data.username)
                    await create_new_user(data.username, email, password)
                    # await set_profile(data.username)  # TODO: save icon
                    remove_token(data.username)
                    # finish create user.
                    self.write(SignUpResult(state='ok'))
                else:
                    self.write(SignUpResult(
                        state='error', error='token or password error'))
            except:  # TODO: check exceptions.
                self.write(SignUpResult(state='error', error='invalid data.'))
