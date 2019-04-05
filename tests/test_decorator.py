import unittest
from unittest.mock import Mock, MagicMock, NonCallableMock
from gapsule.utils.decorators import ajaxquery, unauthenticated, active_authenticated
from gapsule.handlers.Base import BaseHandler


class AjaxQueryTestCase(unittest.TestCase):
    def create_query(self, method, ajax_value):
        render_mock = Mock()
        handle_mock = Mock()
        ajax_arg_mock = Mock(return_value=ajax_value)
        query = NonCallableMock(spec=BaseHandler,
                                get_query_argument=ajax_arg_mock,
                                request=Mock(method=method),
                                render=render_mock,
                                get_template_name=Mock(
                                    return_value='index.html'),
                                )
        return query, handle_mock, render_mock

    def test_post_query(self):
        query, handle_mock, render_mock = self.create_query('POST', '0')
        func = ajaxquery(handle_mock)
        func(query)
        handle_mock.assert_called_once_with(query)
        render_mock.assert_not_called()

    def test_ajax_query(self):
        query, handle_mock, render_mock = self.create_query('GET', '1')
        func = ajaxquery(handle_mock)
        func(query)
        handle_mock.assert_called_once_with(query)
        render_mock.assert_not_called()

    def test_nonajax_query(self):
        query, handle_mock, render_mock = self.create_query('GET', '0')
        func = ajaxquery(handle_mock)
        func(query)
        handle_mock.assert_not_called()
        render_mock.assert_called_once_with('index.html')

    def test_decorator_usage(self):
        query, handle_mock, render_mock = self.create_query('GET', '0')
        @ajaxquery
        def func(self_):
            return handle_mock(self_)
        func(query)
        handle_mock.assert_not_called()
        render_mock.assert_called_once_with('index.html')


class AuthenticatedTestCase(unittest.TestCase):
    def create_query(self, method, user):
        redirect = Mock()
        query = NonCallableMock(spec=BaseHandler,
                                current_user=user,
                                request=Mock(
                                    method=method, fullurl=Mock(return_value='/fullurl'), uri='/uri'),
                                redirect=redirect,
                                get_login_url=Mock(return_value='/login'),
                                get_verify_url=Mock(
                                    return_value='/verify'),
                                )
        return query, redirect

    def test_unauthenticated1(self):
        handle_mock = Mock()
        user = NonCallableMock(user='alice', active=False)
        query, redirect = self.create_query('GET', user)
        f = unauthenticated(handle_mock)
        f(query)
        redirect.assert_called_once()
        handle_mock.assert_not_called()

    def test_unauthenticated2(self):
        handle_mock = Mock()
        user = None
        query, redirect = self.create_query('GET', user)
        f = unauthenticated(handle_mock)
        f(query)
        redirect.assert_not_called()
        handle_mock.assert_called_once_with(query)

    def test_active_authenticated1(self):
        handle_mock = Mock()
        user = NonCallableMock(user='alice', active=False)
        query, redirect = self.create_query('GET', user)
        f = active_authenticated(handle_mock)
        f(query)
        redirect.assert_called_once()
        handle_mock.assert_not_called()

    def test_active_authenticated2(self):
        handle_mock = Mock()
        user = NonCallableMock(user='alice', active=True)
        query, redirect = self.create_query('GET', user)
        f = active_authenticated(handle_mock)
        f(query)
        redirect.assert_not_called()
        handle_mock.assert_called_once_with(query)

    def test_active_authenticated3(self):
        handle_mock = Mock()
        user = None
        query, redirect = self.create_query('GET', user)
        f = active_authenticated(handle_mock)
        f(query)
        redirect.assert_called_once()
        handle_mock.assert_not_called()
