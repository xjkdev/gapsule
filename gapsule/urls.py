import tornado.web
import os

from gapsule.handlers.Main import MainHandler
from gapsule import settings

routes = [
    (r"/", MainHandler),
    (r"/static/(.*)", tornado.web.StaticFileHandler, {
        'path': settings.static_path
    }),
    (r"/.*", MainHandler),
]
