#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient  # Assuming the class is in client.py
from utils import get_json          # get_json should also be in utils.py
from unittest.mock import patch
import fixtures  # assuming fixtures.py exists in the same directory

class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct payload"""
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")


class TestGithubOrgClient(unittest.TestCase):
    # ... previous test_org method ...

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct URL from org data"""
        test_payload = {
            "repos_url": "https://api.github.com/orgs/test-org/repos"
        }

        with patch.object(GithubOrgClient, 'org', new_callable=property) as mock_org:
            mock_org.return_value = test_payload
            client = GithubOrgClient("test-org")
            result = client._public_repos_url
            self.assertEqual(result, test_payload["repos_url"])

class TestGithubOrgClient(unittest.TestCase):
    # ... previous test methods ...

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns expected repo names and calls dependencies once"""
        mock_repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = mock_repos_payload

        with patch.object(GithubOrgClient, "_public_repos_url", new="https://api.github.com/orgs/test-org/repos") as mock_repos_url:
            client = GithubOrgClient("test-org")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/test-org/repos")
            self.assertEqual(mock_repos_url, "https://api.github.com/orgs/test-org/repos")


class TestGithubOrgClient(unittest.TestCase):
    # ... previous test methods ...

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns True if license matches"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)

@parameterized_class([
    {
        "org_payload": fixtures.org_payload,
        "repos_payload": fixtures.repos_payload,
        "expected_repos": fixtures.expected_repos,
        "apache2_repos": fixtures.apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Start patcher for requests.get and configure side effects"""
        cls.get_patcher = patch("requests.get")

        # Start the patcher and assign the mock to cls.mock_get
        cls.mock_get = cls.get_patcher.start()

        # Configure .json() return values depending on the URL
        cls.mock_get.side_effect = [
            MagicMock(json=lambda: cls.org_payload),
            MagicMock(json=lambda: cls.repos_payload)
        ]

    @classmethod
    def tearDownClass(cls):
        """Stop patcher after tests"""
        cls.get_patcher.stop()