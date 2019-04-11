from tornado.escape import json_decode
from tornado.web import HTTPError
from gapsule.handlers.Base import BaseHandler
from gapsule.utils import unauthenticated, ajaxquery
from gapsule.utils.viewmodels import ViewModelDict, ViewModelField
from gapsule.models.user import add_user_pending_verifying, create_new_user


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
    password = ViewModelField(required=True)
    token = ViewModelField(required=True)
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
    def post(self, action=None):
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
                # check pending list
                pending_data = 'pending'
                if data.password == pending_data and data.token == pending_data:
                    self.write(SignUpResult(state='ok'))
                else:
                    self.write(SignUpResult(
                        state='error', error='token or password error'))
            except:  # TODO: check exceptions.
                self.write(SignUpResult(state='error', error='invalid token.'))
        elif action == '/finishing':
            try:
                data = SignUpInputStep2(json_decode(self.request.body))
                # check pending list
                pending_data = 'pending'
                if data.password == pending_data and data.token == pending_data:
                    # finish create user.
                    self.write(SignUpResult(state='ok'))
                else:
                    self.write(SignUpResult(
                        state='error', error='token or password error'))
            except:  # TODO: check exceptions.
                self.write(SignUpResult(state='error', error='invalid data.'))
