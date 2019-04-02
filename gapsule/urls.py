import tornado.web
import os

from gapsule.handlers.Main import MainHandler
from gapsule.handlers.User import Signin
from gapsule.settings import settings
from gapsule.handlers.RepoHandler import (CodeListHandler, FolderListHandler,
                                          FileContentHandler,)
#from gapsule.handlers.PullRequest import (PullRequestPageHandler,)

routes = [
    (r"/", MainHandler),
    (r"/signin", Signin.SignInHandler),
    (r"/static/(.*)", tornado.web.StaticFileHandler, {
        'path': settings['static_path']
    }),
    (r"/?<username>(w+)/?<projectname>(w+)/", CodeListHandler),
    (r"/?<username>(w+)/?<projectname>(w+)/tree/?<branch>(w+)/?<restpath>(^/]+)", FolderListHandler),
    (r"/?<username>(w+)/?<projectname>(w+)/blob/?<branch>(w+)/?<restpath>(^/]+)", FileContentHandler),
    #(r"/(w+)/(w+)/pulls", PullRequestPageHandler),
    (r"/.*", MainHandler),
]
