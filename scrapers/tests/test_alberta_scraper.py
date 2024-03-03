import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import site6

import unittest.mock as mock
import unittest
import requests

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self):
            with open(os.path.dirname(os.path.abspath(__file__)) + "/alberta_get_response.txt", 'r', encoding="utf-8") as f:
                self.text = f.read()
            self.cookies = {}
    
    return MockResponse()

def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, file_name):
            with open(file_name, 'r', encoding="utf-8") as f:
                self.text = f.read()

    last_name_idx = "lastName"
    first_name_idx = "firstName"

    # if kwargs["data"][last_name_idx] == "Maryna" and kwargs["data"][first_name_idx] == "Mammoliti":
    #     return MockResponse(os.path.dirname(os.path.abspath(__file__)) + "/alberta_post_response_MammolitiM.txt")
    
    if kwargs["data"][last_name_idx] == "Amanie" and kwargs["data"][first_name_idx] == "John":
        return MockResponse(os.path.dirname(os.path.abspath(__file__)) + "/alberta_post_response_JohnA.txt")
    
    # if kwargs["data"][last_name_idx] == "Dever" and kwargs["data"][first_name_idx] == "John":
    #     return MockResponse(os.path.dirname(os.path.abspath(__file__)) + "/alberta_post_response_JohnD.txt")
    
    # Couldn't find given args
    assert False

class AlbertaTests(unittest.TestCase):
    
        # @mock.patch('requests.get', side_effect=mocked_requests_get)
        # @mock.patch('requests.post', side_effect=mocked_requests_post)
        # def test_verified(self, mock_get, mock_post):
        #     self.assertEqual(site6.get_status("Maryna", "Mammoliti"), 'Practicing')
    
        @mock.patch('requests.get', side_effect=mocked_requests_get)
        @mock.patch('requests.post', side_effect=mocked_requests_post)
        def test_inactive(self, mock_get, mock_post):
            status = site6.get_status("Amanie", "John")
            print(status)
            self.assertEqual(status, 'Practicing')    
    
        # @mock.patch('requests.get', side_effect=mocked_requests_get)
        # @mock.patch('requests.post', side_effect=mocked_requests_post)
        # def test_not_found(self, mock_get, mock_post):
        #     self.assertEqual(site6.get_status("Dever", "John"), 'Not-Practicing')

if __name__ == "__main__":
    unittest.main()