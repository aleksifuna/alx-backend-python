#!/usr/bin/env python3
"""
utils test classes module
"""
import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch, Mock
from typing import Dict, Tuple, Union


class TestAccessNestedMap(unittest.TestCase):
    """
    Test class for access_nested_map function
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self,
                               nested_map: Dict,
                               path: Tuple[str],
                               expected: Union[Dict, int]
                               ) -> None:
        """Tests the access nested map function"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a", ), "a"),
        ({"a": 1}, ("a", "b"), "b")
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected):
        """
        Tests exception raised on the access nested map function
        """
        with self.assertRaises(KeyError) as e:
            access_nested_map(nested_map, path)
        self.assertEqual(f"KeyError('{expected}')", repr(e.exception))


class TestGetJson(unittest.TestCase):
    """
    Test class for get_json function
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url, test_payload):
        """
        Test method get_json returns correct payload
        """
        config = {'json.return_value': test_payload}
        with patch('requests.get', return_value=Mock(**config)) as req_json:
            self.assertEqual(get_json(test_url), test_payload)
            req_json.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """
    Test class for memoize wrapper function
    """

    def test_memoize(self) -> None:
        """
        Tests memoize wrapper function
        """
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass,
                          'a_method',
                          return_value=lambda: 42
                          ) as mocked_attr:
            test_class = TestClass()
            self.assertEqual(test_class.a_property(), 42)
            self.assertEqual(test_class.a_property(), 42)
            mocked_attr.assert_called_once()
