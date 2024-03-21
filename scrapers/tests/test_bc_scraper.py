import os
import sys
import unittest
import requests
import unittest.mock as mock

# Add parent directoy to sys paths
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# from site1 import confirm_user, get_status
import site1

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self):
            with open(os.path.dirname(os.path.abspath(__file__)) + "/bc_get_response.txt", 'r', encoding="utf-8") as f:
                self.text = f.read()
            self.cookies = {}
    
    return MockResponse()

def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, file_name):
            with open(file_name, 'r', encoding="utf-8") as f:
                self.text = f.read()
    
    assert kwargs["data"]["form_build_id"] == "form-s5oOzyxEnbHQs1dK5VhIFAl-p_kA3Suoba7JsP5IBNg"
    
    if kwargs["data"]["ps_last_name"] == "Gill" and kwargs["data"]["ps_first_name"] == "Amanpreet":
        return MockResponse(os.path.dirname(os.path.abspath(__file__)) + "/BC_post_response_Amanpreet.txt")
    
    if kwargs["data"]["ps_last_name"] == "Zhou" and kwargs["data"]["ps_first_name"] == "Jian":
        return MockResponse(os.path.dirname(os.path.abspath(__file__)) + "/BC_post_response_Zhou.txt")
    
    if kwargs["data"]["ps_last_name"] == "Keen" and kwargs["data"]["ps_first_name"] == "Anthony":
        return MockResponse(os.path.dirname(os.path.abspath(__file__)) + "/BC_post_response_Anthony.txt")
    
    # Couldn't find given args
    assert False

class TestGetUserInfo(unittest.TestCase):
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_verified(self, mock_get, mock_post):
        self.assertEqual(site1.get_status("Amanpreet", "Gill", ''), 'VERIFIED')

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_inactive(self, mock_get, mock_post):
        self.assertEqual(site1.get_status("Jian", "Zhou", ''), 'INACTIVE')    

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_not_found(self, mock_get, mock_post):
        self.assertEqual(site1.get_status("Anthony", "Keen", ''), 'NOT FOUND')   

if __name__ == "__main__":
    unittest.main()


