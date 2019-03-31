import asyncio
import tornado.ioloop
import tornado.web
from gapsule.models.user import create_new_user
from gapsule.urls import routes
from gapsule import settings
from gapsule.models.connection import make_connect
from gapsule.settings import read_config


def make_app():
    app = tornado.web.Application(routes, template_path=settings.template_path)
    read_config(app)
    tmp_loop = asyncio.new_event_loop()
    tmp_loop.run_until_complete(make_connect(app.settings))
    tmp_loop.close()
    return app


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("server runing at http://localhost:8888/")
    tornado.ioloop.IOLoop.current().start()
