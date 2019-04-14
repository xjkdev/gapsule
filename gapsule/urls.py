import tornado.web
import os

from gapsule.handlers.Main import MainHandler
from gapsule.handlers.User import Signin, Signup, Signout
from gapsule.handlers.GitHTTP import GitHTTPHandler, GIT_URL_PATTERNS_REGEX
from gapsule.handlers import Repo, Notification, Forums
from gapsule.settings import settings

routes = [
    (r"/", MainHandler),
    (r"/new", Repo.NewRepoHandler),
    (r"/signout", Signout.SignOutHandler),
    (r"/signin/?", Signin.SignInHandler),
    (r"/signup(/verify|/finishing)?/?", Signup.SignUpHandler),
    (r"/(?P<owner>\w+)/(?P<reponame>\w+)/(?P<posttype>issues|pulls)/(?P<postid>\d+)",
     Forums.ForumHandler),
    (r"/(?P<owner>\w+)/(?P<reponame>\w+)/issues/new", Forums.NewIssueHandler),
    (r"/static/(.*)", tornado.web.StaticFileHandler, {
        'path': settings['static_path']
    }),
    (r"/notification", Notification.NotificationHandler),
    (r"/(\w+)/(\w+)(?:.git)?(" + GIT_URL_PATTERNS_REGEX + ")", GitHTTPHandler),
    (r"/(?P<username>\w+)/(?P<projectname>\w+)/?", Repo.CodeListHandler),
    (r"/(?P<username>\w+)/(?P<projectname>\w+)/tree/(?P<branch>\w+)/(?P<restpath>.*)/?",
     Repo.FolderListHandler),
    (r"/(?P<username>\w+)/(?P<projectname>\w+)/blob/(?P<branch>\w+)/(?P<restpath>.*)/?",
     Repo.FileContentHandler),
    (r"/.*", MainHandler),
]
