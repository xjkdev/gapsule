import tornado.web
import os

from gapsule.handlers.Main import MainHandler
from gapsule.handlers.User import Signin, Signup
from gapsule.settings import settings
from gapsule.handlers.RepoHandler import (CodeListHandler, FolderListHandler,
                                          FileContentHandler,)
#from gapsule.handlers.PullRequest import (PullRequestPageHandler,)

routes = [
    (r"/", MainHandler),
    (r"/signin/?", Signin.SignInHandler),
    (r"/signup(/verify|/finishing)?/?", Signup.SignUpHandler),
    (r"/static/(.*)", tornado.web.StaticFileHandler, {
        'path': settings['static_path']
    }),
    (r"/?p<username>(w+)/?p<projectname>(w+)/", CodeListHandler),
    (r"/?p<username>(w+)/?p<projectname>(w+)/tree/?p<branch>(w+)/?p<restpath>(^/]+)", FolderListHandler),
    (r"/?p<username>(w+)/?p<projectname>(w+)/blob/?p<branch>(w+)/?p<restpath>(^/]+)", FileContentHandler),
    #(r"/(w+)/(w+)/pulls", PullRequestPageHandler),
    (r"/.*", MainHandler),
]
