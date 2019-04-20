import os

from tornado.testing import AsyncHTTPTestCase
from gapsule.app import make_app


class MainHandlerTestCase(AsyncHTTPTestCase):
    def setUp(self):
        super().setUp()
        with open('./gapsule/templates/index.html', 'rb') as f:
            self.indexpage = f.read()
            f.close()

    def get_app(self):
        return make_app()

    def test_main(self):
        static_root = './gapsule/static'
        static_files = [
            '/' + os.path.relpath(os.path.join(root, name), './gapsule')
            for root, dirs, files in os.walk(static_root) for name in files
        ]
        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, self.indexpage)

        for static in static_files:
            response = self.fetch(static)
            self.assertEqual(response.code, 200)
