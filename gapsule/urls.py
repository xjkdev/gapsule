import tornado.web
import os

from gapsule.handlers.Main import MainHandler
from gapsule.handlers.User import Signin
from gapsule.settings import settings

routes = [
    (r"/", MainHandler),
    (r"/signin", Signin.SignInHandler),
    (r"/static/(.*)", tornado.web.StaticFileHandler, {
        'path': settings['static_path']
    }),
    (r"/.*", MainHandler),
]