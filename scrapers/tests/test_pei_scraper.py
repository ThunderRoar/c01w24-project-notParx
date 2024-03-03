import os
import sys
import json

# Add parent directoy to sys paths
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import site5

import unittest.mock as mock
import unittest
import requests

def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, file_name):
            with open(file_name, 'r', encoding="utf-8") as f:
                self.text = f.read()
            self.status_code = 200

    first_name_idx = 0
    last_name_idx = 1
    licence_idx = 2
    
    search_params = json.loads(kwargs["data"]["queryParameters"])["Parameter"]

    if search_params[first_name_idx]["Value"] == "Walid" and search_params[last_name_idx]["Value"] == "Abdelghaffar" and search_params[licence_idx]["Value"] == "8408":
        return MockResponse(os.path.dirname(os.path.abspath(__file__)) + "/pei_post_response_Walid.txt")
    
    if search_params[first_name_idx]["Value"] == "Lenley" and search_params[last_name_idx]["Value"] == "Adams" and search_params[licence_idx]["Value"] == "7016":
        return MockResponse(os.path.dirname(os.path.abspath(__file__)) + "/pei_post_response_Lenley.txt")
    
    if search_params[first_name_idx]["Value"] == "Victoria" and search_params[last_name_idx]["Value"] == "Ziola" and search_params[licence_idx]["Value"] == "8187":
        return MockResponse(os.path.dirname(os.path.abspath(__file__)) + "/pei_post_response_Vic.txt")

    # Couldn't find given args
    assert False

class PEITests(unittest.TestCase):

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_verified_alphanumeric_licence(self, mock_post):
        self.assertEqual(site5.get_status("Walid", "Abdelghaffar", "T8408"), 'VERIFIED')

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_verified_numeric_licence(self, mock_post):
        self.assertEqual(site5.get_status("Lenley", "Adams", "7016"), 'VERIFIED')

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_not_found(self, mock_post):
        self.assertEqual(site5.get_status("Victoria", "Ziola", "8187"), 'NOT_FOUND')      
