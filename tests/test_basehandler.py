from unittest.mock import Mock, NonCallableMock, patch
import unittest
import base64
import json
import datetime

from gapsule import models
from gapsule.handlers.Base import BaseHandler, AuthState
import gapsule.handlers.Base

test_time = datetime.datetime.now().strftime("%Y/%m/%d% %H:%M:%S")


class BaseHandlerTestCase(unittest.TestCase):
    def create_query(self, chk_session_res, session_cookie):
        check_session_status = Mock(return_value=chk_session_res)
        gapsule.handlers.Base.check_session_status = check_session_status
        if session_cookie is not None:
            get_secure_cookie = Mock(return_value=base64.encodebytes(
                json.dumps(session_cookie).encode()))
        else:
            get_secure_cookie = Mock(return_value=None)
        base_handler = NonCallableMock(
            spec=BaseHandler, get_secure_cookie=get_secure_cookie,
            get_current_uesr=BaseHandler.get_current_user
        )
        return base_handler, get_secure_cookie, check_session_status

    def test_get_current_user1(self):
        cookie = dict(user="test-user", session="test-session",
                      logged_time=test_time)
        b, g, c = self.create_query(True, cookie)
        res = BaseHandler.get_current_user(b)
        g.assert_called_with('session')
        c.assert_called_with('test-user', 'test-session')
        self.assertEqual((res.user, res.active), ('test-user', True))

    def test_get_current_user2(self):
        cookie = dict(user="test-user", session="test-session",
                      logged_time=test_time)
        b, g, c = self.create_query(False, cookie)
        res = BaseHandler.get_current_user(b)
        g.assert_called_with('session')
        c.assert_called_with('test-user', 'test-session')
        self.assertEqual((res.user, res.active), ('test-user', False))

    def test_get_current_user3(self):
        cookie = None
        b, g, c = self.create_query(False, cookie)
        res = BaseHandler.get_current_user(b)
        g.assert_called_with('session')
        c.assert_not_called()
        self.assertEqual(res, None)
