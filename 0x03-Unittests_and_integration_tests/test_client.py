#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient  # Assuming the class is in client.py
from utils import get_json          # get_json should also be in utils.py
from unittest.mock import patch

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