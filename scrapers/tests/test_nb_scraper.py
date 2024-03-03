import os
import sys
import json

# Add parent directoy to sys paths
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import site7

import unittest.mock as mock
import unittest
import requests

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, file_name):
            with open(file_name, 'r', encoding="utf-8") as f:
                self.text = f.read()

    if args[0] == "https://cpsnb.alinityapp.com/Client/PublicDirectory/Registrant/0d5ff3f9-6561-ee11-b024-000d3a844429":
        return MockResponse(os.path.dirname(os.path.abspath(__file__)) + "/nb_get_response_Sam.txt")
    
    if args[0] == "https://cpsnb.alinityapp.com/Client/PublicDirectory/Registrant/9f49f3f9-6561-ee11-b024-000d3a844429":
        return MockResponse(os.path.dirname(os.path.abspath(__file__)) + "/nb_get_response_Nizar.txt")
    
    # Couldn't find given args
    assert False


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

    if search_params[first_name_idx]["Value"] == "Samantha" and search_params[last_name_idx]["Value"] == "Ables" and search_params[licence_idx]["Value"] == "11355":
        return MockResponse(os.path.dirname(os.path.abspath(__file__)) + "/nb_post_response_Sam.txt")
    
    if search_params[first_name_idx]["Value"] == "Nizar" and search_params[last_name_idx]["Value"] == "Abdel Samad" and search_params[licence_idx]["Value"] == "4156":
        return MockResponse(os.path.dirname(os.path.abspath(__file__)) + "/nb_post_response_Nizar.txt")
    
    if search_params[first_name_idx]["Value"] == "Eslam" and search_params[last_name_idx]["Value"] == "Abdul" and search_params[licence_idx]["Value"] == "5961":
        return MockResponse(os.path.dirname(os.path.abspath(__file__)) + "/nb_post_response_Eslam.txt")

    # Couldn't find given args
    assert False

class NBTests(unittest.TestCase):

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_verified1(self, mock_get, mock_post):
        self.assertEqual(site7.get_status("Samantha", "Ables", "11355"), 'VERIFIED')

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_verified2(self, mock_get, mock_post):
        self.assertEqual(site7.get_status("Nizar", "Abdel Samad", "4156"), 'VERIFIED')    

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_not_found(self, mock_get, mock_post):
        self.assertEqual(site7.get_status("Eslam", "Abdul", "5961"), 'NOT_FOUND')   
