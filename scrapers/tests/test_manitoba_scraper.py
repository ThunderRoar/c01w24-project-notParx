import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import requests

# Add parent directoy to sys paths
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from site4 import get_user_status, check_status

def mocked_requests_get(*args, **kwargs):
    class MockResponse1:
        def json(self):
            return { "items": [{
                    "descriptions": ["Kaganski", "Emily"],
                    "links": [{"parameters": "123"}]
                }]
            }
    
    class MockResponse2():
        def json(self):
            return { "membershipClass":"Regulated Member - Full" }

    if args[0] == "https://member.cpsm.mb.ca/api/physicianprofile/searchresult?lastname=Saganski&firstname=Emily&fieldofpractice=&city=&postalcode=&wheelchairaccess=&languages=":
        return MockResponse1()
    elif args[0] == "https://member.cpsm.mb.ca/api/physicianprofile/practitionerinformation?id=123":
        return MockResponse2()


class TestUserStatus(unittest.TestCase):

    @patch('site4.requests.get', side_effect=mocked_requests_get)
    def test_get_user_status_success(self, mock_get):       
        self.assertEqual(get_user_status("Emily", "Saganski"), "VERIFIED")

    @patch('site4.requests.get')
    def test_get_user_status_not_found(self, mock_get):
        mock_get.return_value.json.return_value = {}
        self.assertEqual(get_user_status("Stuart", "Koensgen"), "NOT FOUND")

    @patch('site4.requests.get')
    def test_get_user_status_error(self, mock_get):
        mock_get.side_effect = Exception("Mocked error")
        self.assertEqual(get_user_status("Invalid", "User"), "ERROR")

    def test_check_status_verified(self):
        self.assertEqual(check_status("Regulated Member"), "VERIFIED")

    def test_check_status_not_active(self):
        self.assertEqual(check_status(None), "NOT ACTIVE")
        self.assertEqual(check_status("Some other class"), "NOT ACTIVE")

if __name__ == '__main__':
    unittest.main()
