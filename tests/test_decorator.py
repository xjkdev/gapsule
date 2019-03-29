import unittest
from unittest.mock import Mock, MagicMock
from gapsule.utils.decorators import ajaxquery
from tornado.web import RequestHandler


class AjaxQueryTestCase(unittest.TestCase):
    def test_ajax_query(self):
        render_mock = Mock()
        handle_mock = Mock()
        ajax_arg_mock = Mock(return_value='1')
        query = MagicMock(spec=RequestHandler,
                          get_query_argument=ajax_arg_mock,
                          render=render_mock,
                          )
        func = ajaxquery(handle_mock)
        func(query)
        handle_mock.assert_called_once_with(query)
        render_mock.assert_not_called()

    def test_nonajax_query(self):
        render_mock = Mock()
        handle_mock = Mock()
        nonajax_arg_mock = Mock(return_value='0')
        query = MagicMock(spec=RequestHandler,
                          get_query_argument=nonajax_arg_mock,
                          render=render_mock,
                          )
        func = ajaxquery(handle_mock)
        func(query)
        handle_mock.assert_not_called()
        render_mock.assert_called_once_with('index.html')
