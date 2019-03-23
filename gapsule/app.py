import tornado.ioloop
import tornado.web
from gapsule.urls import routes
from gapsule import settings


def make_app():
    return tornado.web.Application(routes, template_path=settings.template_path)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("server runing at http://localhost:8888/")
    tornado.ioloop.IOLoop.current().start()
