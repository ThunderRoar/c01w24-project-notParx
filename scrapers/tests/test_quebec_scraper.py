import unittest
from unittest.mock import patch, MagicMock
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import sys

# Add parent directoy to sys paths
parent_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site10')
sys.path.append(parent_dir)

import quebec_scraper

class TestGetStatus(unittest.TestCase):
    def test_verified(self):
        # Mock for driver
        mock_driver = MagicMock()
        mock_driver.get.return_value = None

        # mock for button and data_element
        mock_button_element = MagicMock()
        mock_button_element.text = 'Inscrit - Actif'
        mock_button_element.click.return_value = None
        mock_driver.find_element.return_value = mock_button_element

        # Patching the selenium methods
        with patch('quebec_scraper.webdriver.Chrome') as mock_driver_class,\
             patch('quebec_scraper.webdriver.support.expected_conditions.visibility_of_element_located'):
            
            mock_driver_class.return_value = mock_driver

            status = quebec_scraper.getStatus('LastName', 'Number')
            self.assertEqual(status, "VERIFIED")
    
    def test_inactive(self):
        # Mock for driver
        mock_driver = MagicMock()
        mock_driver.get.return_value = None

        # mock for button and data_element
        mock_button_element = MagicMock()
        mock_button_element.text = 'Inactive'
        mock_button_element.click.return_value = None
        mock_driver.find_element.return_value = mock_button_element

        # patching the selenium methods
        with patch('quebec_scraper.webdriver.Chrome') as mock_driver_class,\
             patch('quebec_scraper.webdriver.support.expected_conditions.visibility_of_element_located'):
            
            # return the mock when calling 'webdriver.Chrome(options=options)'
            mock_driver_class.return_value = mock_driver

            status = quebec_scraper.getStatus('LastName', 'Number')
            self.assertEqual(status, "INACTIVE")
    def test_not_found_timeout(self):
        # Mock for driver
        mock_driver = MagicMock()
        mock_driver.get.return_value = None

        # mock for button and data_element
        mock_button_element = MagicMock()
        mock_button_element.click.return_value = None
        mock_driver.find_element.return_value = mock_button_element

        # patching the selenium methods
        with patch('quebec_scraper.webdriver.Chrome') as mock_driver_class,\
             patch('quebec_scraper.webdriver.support.expected_conditions.visibility_of_element_located') as mock_timeout:
            mock_timeout.side_effect = TimeoutException()

            # return the mock when calling 'webdriver.Chrome(options=options)'
            mock_driver_class.return_value = mock_driver

            status = quebec_scraper.getStatus('LastName', 'Number')
            self.assertEqual(status, "NOT FOUND")
    def test_not_found_noElement(self):
        # Mock for driver
        mock_driver = MagicMock()
        mock_driver.get.return_value = None

        # mock for button and data_element
        mock_button_element = MagicMock()
        mock_button_element.click.return_value = None
        mock_driver.find_element.return_value = mock_button_element

        # patching the selenium methods
        with patch('quebec_scraper.webdriver.Chrome') as mock_driver_class,\
             patch('quebec_scraper.webdriver.support.expected_conditions.visibility_of_element_located') as mock_timeout:
            mock_timeout.side_effect = NoSuchElementException()

            # return the mock when calling 'webdriver.Chrome(options=options)'
            mock_driver_class.return_value = mock_driver

            status = quebec_scraper.getStatus('LastName', 'Number')
            self.assertEqual(status, "NOT FOUND")
    
if __name__ == '__main__':
    unittest.main()
