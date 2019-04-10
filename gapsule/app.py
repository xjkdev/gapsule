import tornado.ioloop
import tornado.web
import asyncio
from gapsule import settings
import gapsule.models
from gapsule.urls import routes


def make_app():
    app = tornado.web.Application(routes, **settings.settings)
    return app


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("server runing at http://localhost:8888/")
    tornado.ioloop.IOLoop.current().start()
