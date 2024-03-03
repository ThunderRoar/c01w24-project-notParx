import os
import sys

# Add parent directoy to sys paths
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import site1
import unittest.mock as mock, patch, MagicMock
import unittest
import requests

class TestGetUserInfo(unittest.TestCase):
    
    @patch('site1.webdriver')
    def test_get_user_info_verified(self, mock_webdriver):
        mock_browser = MagicMock()
        mock_webdriver.Chrome.return_value = mock_browser

        mock_element = MagicMock()
        mock_element.text = "Amanpreet Gill"
        mock_browser.find_element.return_value = mock_element

        result = get_user_info("Amanpreet", "Gill")
        self.assertEqual(result, "VERIFIED")

    @patch('site1.webdriver')
    def test_get_user_info_not_found(self, mock_webdriver):
        mock_browser = MagicMock()
        mock_webdriver.Chrome.return_value = mock_browser

        mock_element = MagicMock()
        mock_element.text = "Sorry, there are no matching results found. Please try another search."
        mock_browser.find_element.return_value = mock_element

        result = get_user_info("Aalto", "Anu")
        self.assertEqual(result, "NOT FOUND")

    @patch('site1.webdriver')
    def test_get_user_info_exception(self, mock_webdriver):
        mock_browser = MagicMock()
        mock_webdriver.Chrome.return_value = mock_browser

        mock_browser.find_element.side_effect = Exception("Test Exception")

        result = get_user_info("Davey", "Gin")
        self.assertEqual(result, "NOT FOUND")

if __name__ == "__main__":
    unittest.main()
