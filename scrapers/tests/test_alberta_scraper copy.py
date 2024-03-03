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
            self.status_code = 200
            with open(os.path.dirname(os.path.abspath(__file__)) + "/alberta_get_response.txt", 'r', encoding="utf-8") as f:
                self.text = f.read()
            self.content = self.text.encode('utf-8') 
            self.cookies = {}
    if args[0] == "https://search.cpsa.ca/PhysicianProfile?e=a6e336f4-65ab-441f-acce-23cdf1a3324c&i=0":
        False

    return MockResponse()

def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, file_name):
            self.status_code = 200
            with open(file_name, 'r', encoding="utf-8") as f:
                self.text = f.read()
            self.content = self.text.encode('utf-8')

    last_name_idx = "lastName"
    first_name_idx = "firstName"
    
    if kwargs["data"][last_name_idx] == "Amanie" and kwargs["data"][first_name_idx] == "John":
        return MockResponse(os.path.dirname(os.path.abspath(__file__)) + "/alberta_post_response_JohnA.txt")
    
    # Couldn't find given args
    assert False

def mock_open_profile_and_analyze(profile_url):
    class MockResponse:
           def MockResponse(self):
               return True
    #        if profile_url == 'https://search.cpsa.ca/PhysicianProfile?e=a6e336f4-65ab-441f-acce-23cdf1a3324c&i=0':
    #            return False
    # print("heyyy shreyas")
    # if profile_url == 'https://search.cpsa.ca/PhysicianProfile?e=a6e336f4-65ab-441f-acce-23cdf1a3324c&i=0':
    #     print(profile_url)
    #     return True
    return MockResponse()

class AlbertaTests(unittest.TestCase):
    
        #@mock.patch('site6.open_profile_and_analyze', side_effect=mock_open_profile_and_analyze)
        @mock.patch('requests.post', side_effect=mocked_requests_post)
        @mock.patch('requests.get', side_effect=mocked_requests_get)
        def test_inactive(self, mock_post, mock_get):
            status = site6.get_status("Amanie", "John")
            print(status)
            self.assertEqual(status, 'Practicing')

if __name__ == "__main__":
    unittest.main()