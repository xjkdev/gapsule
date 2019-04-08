import tornado.ioloop
import tornado.web

from gapsule import settings
import gapsule.models
from gapsule.urls import routes

from gapsule.models.user import create_new_user, set_profile


def make_app():
    app = tornado.web.Application(routes, **settings.settings)
    return app


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("server runing at http://localhost:8888/")
    tornado.ioloop.IOLoop.current().start()
