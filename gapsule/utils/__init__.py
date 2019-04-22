
from gapsule.utils.decorators import ajaxquery
from gapsule.utils.decorators import active_authenticated, unauthenticated
from tornado.web import authenticated
import asyncio
import functools


def async_test(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        coro = asyncio.coroutine(f)
        future = coro(*args, **kwargs)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(future)
    return wrapper


__all__ = ['ajaxquery', 'active_authenticated',
           'authenticated', 'unauthenticated', 'async_test']
