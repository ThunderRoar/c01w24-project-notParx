import unittest
from unittest.mock import patch, MagicMock
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import sys

# Add parent directoy to sys paths
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import site3

class TestSaskatchewanScraper(unittest.TestCase):
    def test_scrape_table_data(self):
        mock_driver = MagicMock()
        mock_table = MagicMock()
        mock_rows = MagicMock()

        attribute_mock = MagicMock()
        attribute_mock.get_attribute.return_value = 'Profile Link'
       
        profile_mock = MagicMock()
        profile_mock.find_element.return_value = attribute_mock

        cells = [MagicMock(text="Last Name"),
                MagicMock(text="First Name"),
                MagicMock(text="Middle Name"),
                MagicMock(text="City"),
                MagicMock(text="Province"),
                MagicMock(text="Country"),
                MagicMock(text="Language"),
                MagicMock(text="Postal Code"),
                MagicMock(text="Phone"),
                MagicMock(text="Fax"),
                profile_mock]

        mock_driver.find_element.return_value = mock_table
        mock_table.find_elements.return_value = [mock_rows] * 2

        mock_rows.find_elements.return_value = cells

        allrows = site3.scrape_table_data(mock_driver)
        correct = [{
            'LastName': 'Last Name',
            'FirstName': 'First Name',
            'MiddleName': 'Middle Name',
            'City': 'City',
            'Province': 'Province',
            'Country': 'Country',
            'Language': 'Language',
            'PostalCode': 'Postal Code',
            'Phone': 'Phone',
            'Fax': 'Fax',
            'ProfileLink': 'Profile Link'
            }]
        self.assertEqual(allrows, correct)

    def test_check_status_on_register_True(self):
        mock_driver = MagicMock()
        mock_driver.get.return_value = None

        mock_status_element = MagicMock(text='On the Register')
        mock_driver.find_element.return_value = mock_status_element
        
        with patch('site3.webdriver.support.expected_conditions.presence_of_element_located'):
            answer = site3.check_status_on_register(mock_driver, '')
            self.assertEqual(answer, "VERIFIED")

    def test_check_status_on_register_False(self):
        mock_driver = MagicMock()
        mock_driver.get.return_value = None

        mock_status_element = MagicMock(text='Not on register')
        mock_driver.find_element.return_value = mock_status_element
        
        with patch('site3.webdriver.support.expected_conditions.presence_of_element_located'):
            answer = site3.check_status_on_register(mock_driver, '')
            self.assertEqual(answer, "INACTIVE")

    def test_getStatus_with_mocked_functions(self):
        with patch('site3.saskatchewan_scraper.initialize_webdriver') as mock_initialize,\
            patch('site3.saskatchewan_scraper.submit_search_form') as mock_submit,\
            patch('site3.saskatchewan_scraper.scrape_table_data') as mock_scrape,\
            patch('site3.saskatchewan_scraper.check_status_on_register') as mock_check_status:

            mock_initialize.return_value = MagicMock()
            mock_submit.return_value = None
            mock_scrape.return_value = [{'FirstName': 'John', 'LastName': 'Doe', 'ProfileLink': 'http://example.com'}]
            mock_check_status.return_value = "VERIFIED"

            status = site3.saskatchewan_scraper.getStatus("John", "Doe")
            self.assertEqual(status, "VERIFIED")

if __name__ == '__main__':
    unittest.main()