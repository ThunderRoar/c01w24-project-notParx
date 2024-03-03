import os
import sys

# Add parent directoy to sys paths
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import site2

import unittest.mock as mock
import unittest
import requests

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self):
            with open(os.path.dirname(os.path.abspath(__file__)) + "/ontario_get_response.txt", 'r', encoding="utf-8") as f:
                self.text = f.read()
            self.cookies = {}
    
    return MockResponse()

def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, file_name):
            with open(file_name, 'r', encoding="utf-8") as f:
                self.text = f.read()

    last_name_idx = "p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$txtLastName"
    first_name_idx = "p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$txtFirstName"
    prescriber_idx = "p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$txtCPSONumberGeneral"  
    
    if kwargs["data"][last_name_idx] == "Edwards" and kwargs["data"][first_name_idx] == "Bonnie" and kwargs["data"][prescriber_idx] == 30722:
        return MockResponse(os.path.dirname(os.path.abspath(__file__)) + "/ontario_post_response_Bonnie.txt")
    
    if kwargs["data"][last_name_idx] == "Aaen" and kwargs["data"][first_name_idx] == "Gregory" and kwargs["data"][prescriber_idx] == 89942:
        return MockResponse(os.path.dirname(os.path.abspath(__file__)) + "/ontario_post_response_GregA.txt")
    
    if kwargs["data"][last_name_idx] == "Pins" and kwargs["data"][first_name_idx] == "Gregory" and kwargs["data"][prescriber_idx] == 54111:
        return MockResponse(os.path.dirname(os.path.abspath(__file__)) + "/ontario_post_response_GregP.txt")
    
    # Couldn't find given args
    assert False

class OntarioTests(unittest.TestCase):

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_verified(self, mock_get, mock_post):
        self.assertEqual(site2.get_status("Edwards", "Bonnie", 30722), 'VERIFIED')

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_inactive(self, mock_get, mock_post):
        self.assertEqual(site2.get_status("Aaen", "Gregory", 89942), 'INACTIVE')    

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_not_found(self, mock_get, mock_post):
        self.assertEqual(site2.get_status("Pins", "Gregory", 54111), 'NOT FOUND')   
