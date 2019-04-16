import tornado.web

from gapsule.handlers.Main import MainHandler
from gapsule.handlers.User import Signin, Signup, Signout
from gapsule.handlers.GitHTTP import GitHTTPHandler, GIT_URL_PATTERNS_REGEX
from gapsule.handlers import Repo, Notification, Forums, PullRequest
from gapsule.settings import settings

routes = [
    (r"/", MainHandler),
    (r"/new", Repo.NewRepoHandler),
    (r"/signout", Signout.SignOutHandler),
    (r"/signin/?", Signin.SignInHandler),
    (r"/signup(/verify|/finishing)?/?", Signup.SignUpHandler),
    (r"/(?P<owner>\w+)/(?P<reponame>\w+)/(?P<posttype>issues|pulls)/?",
     Forums.PostListHandler),
    (r"/(?P<owner>\w+)/(?P<reponame>\w+)/(?P<posttype>issues|pull)/(?P<postid>\d+)",
     Forums.ForumHandler),
    (r"/(?P<owner>\w+)/(?P<reponame>\w+)/issues/new", Forums.NewIssueHandler),
    (r"/static/(.*)", tornado.web.StaticFileHandler, {
        'path': settings['static_path']
    }),
    (r"/notification", Notification.NotificationHandler),
    (r"/(\w+)/(\w+)(?:.git)?(" + GIT_URL_PATTERNS_REGEX + ")", GitHTTPHandler),
    (r"/(?P<owner>\w+)/(?P<reponame>\w+)/?", Repo.CodeListHandler),
    (r"/(?P<owner>\w+)/(?P<reponame>\w+)/tree/(?P<branch>\w+)/(?P<restpath>.*)/?",
     Repo.FolderListHandler),
    (r"/(?P<owner>\w+)/(?P<reponame>\w+)/blob/(?P<branch>\w+)/(?P<restpath>.*)/?",
     Repo.FileContentHandler),
    (r"/(?P<owner>\w+)/(?P<reponame>\w+)/pull/(?P<postid>\d+)/commits/?",
     PullRequest.PullCommitsHandler),
    (r"/(?P<owner>\w+)/(?P<reponame>\w+)/pull/(?P<postid>\d+)/checks/?",
     PullRequest.PullChecksHandler),
    (r"/(?P<owner>\w+)/(?P<reponame>\w+)/pull/(?P<postid>\d+)/files/?",
     PullRequest.PullFilesHandler),
    (r"/(?P<owner>\w+)/(?P<reponame>\w+)/compare/(?P<restpath>.*)/?",
     PullRequest.CreatePullRequestHandler),
    (r"/.*", MainHandler),
]
