from tornado.testing import AsyncHTTPTestCase
from gapsule.app import make_app


class SignInHandlerTestCase(AsyncHTTPTestCase):
    def get_app(self):
        return make_app()

    def test_signin(self):
        response = self.fetch('/signin')
        self.assertEqual(response.code, 200)
