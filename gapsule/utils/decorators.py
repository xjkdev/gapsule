from tornado.web import RequestHandler, HTTPError, urlencode
import urllib
import functools


def ajaxquery(f, template_name='index.html', **kwargs):
    """ Decorated function only runs if ajax-querying, otherwise render 'index.html'. """
    @functools.wraps(f)
    def _wrapper(self, *args, **kwargs):
        if self.request.method in ("GET", "HEAD") and not self.get_query_argument('ajax', '0') == '1':
            self.render(template_name, **kwargs)
            return None
        else:
            return f(self, *args, **kwargs)
    return _wrapper


def active_authenticated(f):
    """ Decorate an function only runs when if current user is signed and active. 
        When not signed, redirect to login_url.
        When not active, redirect to verify_url. """
    @functools.wraps(f)
    def _wrapper(self, *args, **kwargs):
        if not (self.current_user and self.current_user.active is True):
            if self.request.method in ("GET", "HEAD"):
                url = self.get_login_url() if not self.current_user else self.get_verify_url()
                if "?" not in url:
                    if urllib.parse.urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()
                    else:
                        assert self.request.uri is not None
                        next_url = self.request.uri
                    url += "?" + urlencode(dict(next=next_url))
                self.redirect(url)
                return None
            raise HTTPError(403)
        return f(self, *args, **kwargs)
    return _wrapper


def unauthenticated(f, url='/'):
    """ Decorate an function that only run when user unauthenticated. """
    @functools.wraps(f)
    def _wrapper(self, *args, **kwargs):
        nonlocal url
        if self.current_user:
            if self.request.method in ("GET", "HEAD"):
                if "?" not in url:
                    if urllib.parse.urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()
                    else:
                        assert self.request.uri is not None
                        next_url = self.request.uri
                    url += "?" + urlencode(dict(next=next_url))
                self.redirect(url)
                return None
            raise HTTPError(403)
        return f(self, *args, **kwargs)
    return _wrapper
