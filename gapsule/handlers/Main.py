from gapsule.handlers.Base import BaseHandler


class MainHandler(BaseHandler):
    def get(self):
        self.render("index.html")
