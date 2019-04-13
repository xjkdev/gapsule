import tornado.web

from gapsule.handlers.Main import MainHandler
from gapsule.handlers.User import Signin, Signup
from gapsule.handlers.GitHTTP import GitHTTPHandler, GIT_URL_PATTERNS_REGEX
from gapsule.settings import settings
from gapsule.handlers.Repo import (CodeListHandler, FolderListHandler,
                                   FileContentHandler,)
from gapsule.handlers.PullRequest import (CreatePullRequest, NewPullRequest,
                                          NewPullCommits, NewPullFiles, NewPullChecks, NewPullFileDiff,)

routes = [
    (r"/", MainHandler),
    (r"/signin/?", Signin.SignInHandler),
    (r"/signup(/verify|/finishing)?/?", Signup.SignUpHandler),
    (r"/static/(.*)", tornado.web.StaticFileHandler, {
        'path': settings['static_path']
    }),
    (r"/(\w+)/(\w+)(?:.git)?(" + GIT_URL_PATTERNS_REGEX + ")", GitHTTPHandler),
    (r"/(?P<username>\w+)/(?P<projectname>\w+)/?", CodeListHandler),
    (r"/(?P<username>\w+)/(?P<projectname>\w+)/tree/(?P<branch>\w+)/(?P<restpath>.*)/?", FolderListHandler),
    (r"/(?P<username>\w+)/(?P<projectname>\w+)/blob/(?P<branch>\w+)/(?P<restpath>.*)/?",
     FileContentHandler),
    (r"/(?P<username>\w+)/(?P<projectname>\w+)/pull/(?P<libnumber>\d+)/?", NewPullRequest),
    (r"/(?P<username>\w+)/(?P<projectname>\w+)/pull/(?P<libnumber>\d+)/commits/?", NewPullCommits),
    (r"/(?P<username>\w+)/(?P<projectname>\w+)/pull/(?P<libnumber>\d+)/checks/?", NewPullChecks),
    (r"/(?P<username>\w+)/(?P<projectname>\w+)/pull/(?P<libnumber>\d+)/files/?", NewPullFiles),
    (r"/(?P<username>\w+)/(?P<projectname>\w+)/pull/(?P<libnumber>\d+)/files#diff-(?P<path>\w+)/?", NewPullFileDiff),
    (r"/(?P<username>\w+)/(?P<projectname>\w+)/compare/(?P<restpath>.*)/?", CreatePullRequest),
    (r"/.*", MainHandler),
]
