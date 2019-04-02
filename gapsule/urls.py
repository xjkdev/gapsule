import tornado.web
import os

from gapsule.handlers.Main import MainHandler
from gapsule import settings
from gapsule.handlers.RepoHandler import (CodeListHandler, FolderListHandler,
                                          FileContentHandler)

routes = [
    (r"/", MainHandler),
    (r"/static/(.*)", tornado.web.StaticFileHandler, {
        'path': settings.static_path
    }),
    (r"/(w+)/", CodeListHandler),
    (r"/(w+)/tree/(w+)/(^/]+)", FolderListHandler),
    (r"/(w+)/blob/(w+)/(^/]+)", FileContentHandler),
]
