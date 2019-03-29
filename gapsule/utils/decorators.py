from tornado.web import RequestHandler
import typing


def ajaxquery(f):
    """ Run decorated function if ajax-querying, otherwise render 'index.html'. """

    def _wrapper(self_, *args, **kwargs):
        if self_.get_query_argument('ajax', '0') == '1':
            f(self_, *args, **kwargs)
        else:
            self_.render('index.html')
    return _wrapper
