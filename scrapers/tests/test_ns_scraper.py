import os
import sys

# Add parent directoy to sys paths
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import site9

import unittest.mock as mock
import unittest
import requests

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self):
            with open(os.path.dirname(os.path.abspath(__file__)) + "/ns_get_response.txt", 'r', encoding="utf-8") as f:
                self.text = f.read()
            self.cookies = {}
    
    return MockResponse()

def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, file_name):
            with open(file_name, 'r', encoding="utf-8") as f:
                self.text = f.read()

    last_name_idx = "lastname"
    first_name_idx = "firstname"
    prescriber_idx = "licencenumber"
    
    if kwargs["data"][last_name_idx] == "Ley" and kwargs["data"][first_name_idx] == "David" and kwargs["data"][prescriber_idx] == 10819:
        return MockResponse(os.path.dirname(os.path.abspath(__file__)) + "/ns_post_response_DavidL.txt")
    
    if kwargs["data"][last_name_idx] == "Abriel" and kwargs["data"][first_name_idx] == "David" and kwargs["data"][prescriber_idx] == 6371:
        return MockResponse(os.path.dirname(os.path.abspath(__file__)) + "/ns_post_response_DavidA.txt")
    
    if kwargs["data"][last_name_idx] == "Bent" and kwargs["data"][first_name_idx] == "Wilfrid" and kwargs["data"][prescriber_idx] == 5492:
        return MockResponse(os.path.dirname(os.path.abspath(__file__)) + "/ns_post_response_Wilfrid.txt")
    
    if kwargs["data"][last_name_idx] == "Finley" and kwargs["data"][first_name_idx] == "Allen" and kwargs["data"][prescriber_idx] == 7959:
        return MockResponse(os.path.dirname(os.path.abspath(__file__)) + "/ns_post_response_Allen.txt")
    
    # Couldn't find given args
    assert False

class NSTests(unittest.TestCase):

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_verified(self, mock_get, mock_post):
        self.assertEqual(site9.get_status("David", "Ley", 10819), 'VERIFIED')

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_inactive1(self, mock_get, mock_post):
        self.assertEqual(site9.get_status("David", "Abriel", 6371), 'INACTIVE')

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_inactive2(self, mock_get, mock_post):
        self.assertEqual(site9.get_status("Wilfrid", "Bent", 5492), 'INACTIVE')   

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_not_found(self, mock_get, mock_post):
        self.assertEqual(site9.get_status("Allen", "Finley", 7959), 'NOT FOUND')   
