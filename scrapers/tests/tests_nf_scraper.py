import os 
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)


import unittest
import unittest.mock as mock
import site8  

import requests

def mocked_requests_get(*args, **kwargs):
    # Mocked response for the initial search page
    class MockResponse:
        def __init__(self):
            self.status_code = 200
            with open(os.path.dirname(os.path.abspath(__file__))+"/nf_get_response.txt", 'r', encoding="utf-8") as f:
                self.text = f.read()
            self.cookies = {}
            self.content = self.text.encode('utf-8')
    
    return MockResponse()

def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, file_name):
            self.status_code = 200
            with open(file_name, 'r', encoding="utf-8") as f:
                self.text = f.read()
            self.content = self.text.encode('utf-8')
            
    prescriber_idx = "ctl00$TemplateBody$WebPartManager1$gwpciNewQueryMenuCommon$ciNewQueryMenuCommon$ResultsGrid$Sheet0$Input0$TextBox1"
    first_name_idx = "ctl00$TemplateBody$WebPartManager1$gwpciNewQueryMenuCommon$ciNewQueryMenuCommon$ResultsGrid$Sheet0$Input2$TextBox1"
    last_name_idx = "ctl00$TemplateBody$WebPartManager1$gwpciNewQueryMenuCommon$ciNewQueryMenuCommon$ResultsGrid$Sheet0$Input1$TextBox1"

    # Determine which response to send based on form data
    if kwargs["data"][prescriber_idx] == "F 01923" and kwargs["data"][first_name_idx] == "John" and kwargs["data"][last_name_idx] == "Abbatt":
        return MockResponse(os.path.dirname(os.path.abspath(__file__)) + "/nf_post_response_JohnAbbatt.txt")
    
    if kwargs["data"][prescriber_idx] == "F 03818" and kwargs["data"][first_name_idx] == "William" and kwargs["data"][last_name_idx] == "Durocher":
        return MockResponse(os.path.dirname(os.path.abspath(__file__)) + "/nf_post_response_WilliamDurocher.txt")
    

    else:
        assert False

class NfTests(unittest.TestCase):
    @mock.patch('site8.requests.Session.get', side_effect=mocked_requests_get)
    @mock.patch('site8.requests.Session.post', side_effect=mocked_requests_post)
    def test_practicing_status(self, mock_post, mock_get):
        # Test for a physician with practicing status
        result = site8.perform_search("F 01923", "John", "Abbatt")
        self.assertEqual(result, "Non-Practicing")

    @mock.patch('site8.requests.Session.get', side_effect=mocked_requests_get)
    @mock.patch('site8.requests.Session.post', side_effect=mocked_requests_post)
    def test_non_practicing_status(self, mock_post, mock_get):
        result = site8.perform_search("F 03818", "William", "Durocher")
        self.assertEqual(result, "Practicing")
if __name__ == '__main__':
    unittest.main()
