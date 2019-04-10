from unittest.mock import Mock, NonCallableMock, patch
import unittest
from datetime import timedelta
import asyncio

from gapsule import models
from gapsule.handlers.Base import BaseHandler, AuthState
from gapsule.utils.cookie_session import format_log_time, session_encode, datetime_now
from gapsule.utils import async_test
import gapsule.handlers.Base

test_time = format_log_time(datetime_now() - timedelta(seconds=1))


class BaseHandlerTestCase(unittest.TestCase):
    def create_query(self, chk_session_res, session_cookie):
        check_session_status = Mock(return_value=chk_session_res)
        gapsule.handlers.Base.check_session_status = asyncio.coroutine(
            check_session_status)
        if session_cookie is not None:
            get_secure_cookie = Mock(
                return_value=session_encode(session_cookie))
        else:
            get_secure_cookie = Mock(return_value=None)
        base_handler = NonCallableMock(
            spec=BaseHandler, get_secure_cookie=get_secure_cookie,
            prepare=BaseHandler.prepare
        )
        return base_handler, get_secure_cookie, check_session_status

    @async_test
    async def test_get_current_user1(self):
        cookie = dict(user="test-user", session="test-session",
                      logged_time=test_time)
        b, g, c = self.create_query(True, cookie)
        await BaseHandler.prepare(b)
        res = b.current_user
        self.assertEqual((res.user, res.active), ('test-user', True))
        g.assert_called_with('session')
        c.assert_called_with('test-user', 'test-session')

    @async_test
    async def test_get_current_user2(self):
        cookie = dict(user="test-user", session="test-session",
                      logged_time=test_time)
        b, g, c = self.create_query(False, cookie)
        await BaseHandler.prepare(b)
        res = b.current_user
        self.assertEqual((res.user, res.active), ('test-user', False))
        g.assert_called_with('session')
        c.assert_called_with('test-user', 'test-session')

    @async_test
    async def test_get_current_user3(self):
        cookie = None
        b, g, c = self.create_query(False, cookie)
        await BaseHandler.prepare(b)
        res = b.current_user
        self.assertEqual(res, None)
        g.assert_called_with('session')
        c.assert_not_called()
