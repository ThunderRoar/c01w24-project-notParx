import unittest
import unittest.mock as mock
import os
import sys

# Add parent directoy to sys paths
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import site3

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, filename):
            with open(os.path.dirname(os.path.abspath(__file__)) + filename, 'r', encoding="utf-8") as f:
                self.text = f.read()
            self.cookies = {}
    
    if args[0] == "https://www.cps.sk.ca/imis/":
        return MockResponse("/sk_get_token_response.txt")

    assert kwargs["headers"]["Requestverificationtoken"] == "pIQyszjZHkdu7S3zXfpzWIDjVQ0deA5eFgViTKlUWq_BtbJATdgLJfQktnGQcuwUSvGda0NhIh4sib5873eMZUMNCrM1"

    if "Webster" in args[0]:
        return MockResponse("/sk_get_response_Webster.txt")
    if "Not123" in args[0]:
        return MockResponse("/sk_get_response_Not.txt")
    if "Moodley" in args[0]:
        return MockResponse("/sk_get_response_Moodley.txt")

    # Couldn't find given args
    assert False

class TestSaskatchewanScraper(unittest.TestCase):
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_verified(self, mock_get):
        self.assertEqual(site3.get_status("Brittni", "Webster", ''), 'VERIFIED')

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_inactive(self, mock_get):
        self.assertEqual(site3.get_status("Shreya", "Moodley", ''), 'INACTIVE')    

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_not_found(self, mock_get):
        self.assertEqual(site3.get_status("Not123", "Not123", ''), 'NOT FOUND')  

if __name__ == '__main__':
    unittest.main()