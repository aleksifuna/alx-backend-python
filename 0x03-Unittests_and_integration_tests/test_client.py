#!/usr/bin/env python3
"""
GithurbOrgClient test class defination
"""
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from parameterized import parameterized, parameterized_class
import unittest
from unittest.mock import patch, PropertyMock


class TestGithubOrgClient(unittest.TestCase):
    """
    TestGithubOrgClient class defination
    """

    @parameterized.expand([
        ('google'),
        ('abc')
    ])
    @patch('client.get_json')
    def test_org(self, input, mock):
        """
        Tests that get_json was called once with expected arguments
        """
        test_class = GithubOrgClient(input)
        test_class.org()
        test_class.org()
        mock.assert_called_once_with(f'https://api.github.com/orgs/{input}')

    def test_public_repos_url(self):
        """
        Tests that _public_repos_url return a known payload
        """

        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock:
            payload = {'repos_url': 'alex.com'}
            mock.return_value = payload
            test_class = GithubOrgClient('test')
            self.assertEqual(test_class._public_repos_url,
                             payload['repos_url'])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Tests that public_repos method returns appropriet list
        """
        payload = [{'name': 'alx'}, {'name': 'abc'}]
        mock_get_json.return_value = payload

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_pub_repos_url:
            mock_pub_repos_url.return_value = 'Hello World'
            test_class = GithubOrgClient('test')
            public_repos = test_class.public_repos()
            expected = [item['name'] for item in payload]
            self.assertEqual(public_repos, expected)
            mock_get_json.assert_called_once()
            mock_pub_repos_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, results):
        """
        Test has_license method returns expected results
        """
        test_class = GithubOrgClient('google')
        license = test_class.has_license(repo, license_key)
        self.assertEqual(license, results)


@parameterized_class(
    ('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration Test class for GithubOrgClient
    """
    @classmethod
    def setUpClass(cls) -> None:
        """
        Set-up for the intergration tests
        """
        config = {
            'return_value.json.side_effect': [
                cls.org_payload, cls.repos_payload,
                cls.org_payload, cls.repos_payload
            ]
        }
        cls.get_patcher = patch('requests.get', **config)
        cls.mock = cls.get_patcher.start()

    def test_public_repos(self):
        """
        Intergation test for public_repos method
        """
        test_class = GithubOrgClient('google')

        self.assertEqual(test_class.org, self.org_payload)
        self.assertEqual(test_class.repos_payload, self.repos_payload)
        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos('FAKE'), [])
        self.mock.assert_called()

    def test_public_repos_with_license(self) -> None:
        """
        Intergration test for public repos with license
        """
        test_class = GithubOrgClient('google')
        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos('FAKE'), [])
        self.assertEqual(test_class.public_repos('apache-2.0'),
                         self.apache2_repos)

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Teardown for test class
        """
        cls.get_patcher.stop()
