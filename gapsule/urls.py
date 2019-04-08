import tornado.web
import os

from gapsule.handlers.Main import MainHandler
from gapsule.handlers.User import Signin
from gapsule.settings import settings
from gapsule.handlers.RepoHandler import (CodeListHandler, FolderListHandler,
                                          FileContentHandler,)

routes = [
    (r"/", MainHandler),
    (r"/signin", Signin.SignInHandler),
    (r"/static/(.*)", tornado.web.StaticFileHandler, {
       'path': settings['static_path']
    }),
    (r"/(?P<username>\w+)/(?P<projectname>\w+)/?", CodeListHandler),
    (r"/(?P<username>\w+)/(?P<projectname>\w+)/tree/(?P<branch>\w+)/(?P<restpath>.*)/?", FolderListHandler),
    (r"/(?P<username>\w+)/(?P<projectname>\w+)/blob/(?P<branch>\w+)/(?P<restpath>.*)/?", FileContentHandler),
    (r"/.*", MainHandler),
]
