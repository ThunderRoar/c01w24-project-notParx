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
        def __init__(self, text, status_code=200):
            self.text = text
            self.status_code = status_code
            self.content = self.text.encode('utf-8')

    # Mapping URLs to their responses
    url_to_response = {
        "https://search.cpsa.ca/PhysicianProfile?e=a6e336f4-65ab-441f-acce-23cdf1a3324c&i=0": '/alberta_get_response_JohnA.txt',
        "https://search.cpsa.ca/PhysicianProfile?e=cce8302c-4d89-469c-831f-c28f4cff3af2&i=0": '/alberta_get_response_WilliamA.txt',
        # Add more URLs and their corresponding response file paths or HTML strings here
    }

    requested_url = args[0]

    if requested_url in url_to_response:
        response_source = url_to_response[requested_url]
        with open(os.path.dirname(os.path.abspath(__file__)) + response_source, 'r', encoding="utf-8") as f:
            response_content = f.read()
    else:
        # Default response if URL not in the mapping
        with open(os.path.dirname(os.path.abspath(__file__)) + "/alberta_get_response.txt", 'r', encoding="utf-8") as f:
            response_content = f.read()

    return MockResponse(response_content)


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
    
    if kwargs["data"][last_name_idx] == "Atherton" and kwargs["data"][first_name_idx] == "William":
        return MockResponse(os.path.dirname(os.path.abspath(__file__)) + "/alberta_post_response_WilliamA.txt")
    
    # Couldn't find given args
    assert False


class AlbertaTests(unittest.TestCase):
    
        @mock.patch('requests.post', side_effect=mocked_requests_post)
        @mock.patch('requests.get', side_effect=mocked_requests_get)
        def test_inactive(self, mock_post, mock_get):
            self.assertEqual(site6.get_status("Amanie", "John"), 'Practicing')
        
        @mock.patch('requests.post', side_effect=mocked_requests_post)
        @mock.patch('requests.get', side_effect=mocked_requests_get)
        def test_verified(self, mock_post, mock_get):
            self.assertEqual(site6.get_status("Atherton", "William"), 'Non-Practicing')

if __name__ == "__main__":
    unittest.main()