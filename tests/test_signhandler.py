import json
from tornado.testing import AsyncHTTPTestCase
from gapsule.app import make_app


class SignInHandlerTestCase(AsyncHTTPTestCase):
    def get_app(self):
        return make_app()

    def test_get_signin(self):
        response = self.fetch('/signin')
        self.assertEqual(response.code, 200)


class SignUpHandlerTestCase(AsyncHTTPTestCase):
    def get_app(self):
        return make_app()

    def test_get_signup(self):
        response = self.fetch('/signup')
        self.assertEqual(response.code, 200)

    def test_post_signup(self):
        response = self.fetch('/signup',
                              method="POST",
                              body=json.dumps(
                                  dict(username='abcd',
                                       email="abc@ab.com",
                                       password="feafajkljkljL0")))
        # self.assertEqual(response.body, b'{"state": "ok", "token": "Token"}')
        self.assertEqual(response.code, 200)
