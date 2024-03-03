import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import requests
from selenium.common.exceptions import WebDriverException

# Add parent directoy to sys paths
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from site1 import confirm_user, get_user_info

# class TestGetUserInfo(unittest.TestCase):

#     @patch('site1.webdriver')
#     def test_get_user_info_verified(self, mock_webdriver):
#         mock_browser = MagicMock()
#         mock_webdriver.Chrome.return_value = mock_browser
#         mock_element = MagicMock()
#         mock_element.text = "Amanpreet Gill"
#         mock_browser.find_element.side_effect = [mock_element, MagicMock(text="Practising")]
        
#         result = get_user_info("Amanpreet", "Gill")
#         self.assertEqual(result, "VERIFIED")

#     @patch('site1.webdriver')
#     def test_get_user_info_not_found(self, mock_webdriver):
#         mock_browser = MagicMock()
#         mock_webdriver.Chrome.return_value = mock_browser
#         mock_element = MagicMock()
#         mock_element.text = "Sorry, there are no matching results found. Please try another search."
#         mock_browser.find_element.return_value = mock_element
        
#         result = get_user_info("Aalto", "Anu")
#         self.assertEqual(result, "NOT FOUND")

#     @patch('site1.webdriver')
#     def test_get_user_info_practising(self, mock_webdriver):
#         mock_browser = MagicMock()
#         mock_webdriver.Chrome.return_value = mock_browser
#         mock_element = MagicMock()
#         mock_element.text = "Davey Gin"
#         mock_browser.find_element.side_effect = [mock_element, MagicMock(text="Not practising")]
        
#         result = get_user_info("Davey", "Gin")
#         self.assertEqual(result, "VERIFIED")

#     @patch('site1.webdriver')
#     def test_get_user_info_exception(self, mock_webdriver):
#         mock_webdriver.Chrome.side_effect = Exception
        
#         result = get_user_info("Ian", "Gillespie")
#         self.assertEqual(result, "NOT FOUND")

# if __name__ == "__main__":
#     unittest.main()


class TestGetUserInfo(unittest.TestCase):

    @patch('site1.webdriver')
    def test_get_user_info_verified(self, mock_webdriver):
        mock_browser = MagicMock()
        mock_webdriver.Chrome.return_value = mock_browser
        mock_element = MagicMock()
        mock_element.text = "Amanpreet Gill"
        mock_browser.find_element.side_effect = [mock_element, MagicMock(text="Practising")]
        result = get_user_info("Amanpreet", "Gill")
        print("TEST 5")
        self.assertEqual(result, "VERIFIED")

    @patch('site1.webdriver')
    def test_get_user_info_not_found(self, mock_webdriver):
        mock_browser = MagicMock()
        mock_webdriver.Chrome.return_value = mock_browser
        mock_element = MagicMock()
        mock_element.text = "Sorry, there are no matching results found. Please try another search."
        mock_browser.find_element.return_value = mock_element
        result = get_user_info("Aalto", "Anu")
        print("TEST 4")
        self.assertEqual(result, "NOT FOUND")

    @patch('site1.webdriver')
    def test_get_user_info_practising(self, mock_webdriver):
        mock_browser = MagicMock()
        mock_webdriver.Chrome.return_value = mock_browser
        mock_element = MagicMock()
        mock_element.text = "Davey Gin"
        mock_browser.find_element.side_effect = [mock_element, MagicMock(text="Not practising")]
        result = get_user_info("Davey", "Gin")
        print("TEST 3")
        self.assertEqual(result, "VERIFIED")

    @patch('site1.webdriver')
    def test_get_user_info_browser_error(self, mock_webdriver):
        mock_browser = MagicMock()
        mock_webdriver.Chrome.return_value = None
        mock_element = MagicMock()
        mock_element.text = "Sorry, there are no matching results found. Please try another search."
        mock_browser.find_element.return_value = mock_element
        result = get_user_info("Anthony", "Keen")
        print("TEST 2")
        self.assertEqual(result, "NOT FOUND")

    def test_confirm_user(self):
        print("TEST 1")
        text = "Amanpreet Gill"
        self.assertTrue(confirm_user("Amanpreet", "Gill", text))
        self.assertTrue(confirm_user("Gill", "Amanpreet", text))
        self.assertFalse(confirm_user("Anu", "Aalto", text))
        self.assertFalse(confirm_user("Aalto", "Anu", text))

if __name__ == "__main__":
    unittest.main()


