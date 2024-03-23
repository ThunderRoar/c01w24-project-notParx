import unittest
# from unittest.mock import patch, MagicMock
import unittest.mock as mock
import os
import sys
import json

# Add parent directoy to sys paths
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import site10

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        # on init, sets self text to have an id equal to '123' + the original id. Should be parsed by program correctly
        def __init__(self):
            url = args[0]
            sidx = url.find("?number=")
            eidx = url.find("&lastname=")
            person_id = url[sidx + 8:eidx]
            self.text = 'bla bla some HTLM and Code here..$MVmgt5UHrw:[{physicianId:'+ "123" + person_id + ', formattedLabel: "Shalaby, Karam (77587)",lastname: "Shalaby", firstname: "Karam", number: "77587", city: "Beaconsfield"}], bla bla some more lists [booho bad data]'
    
    return MockResponse()

def mocked_requests_post(*args, **kwargs):

    class MockResponse:
        def __init__(self, first, last, status):
            self.text = '''{
    "physicianId": 50068152,
    "formattedLabel": "Li, Annie (15332)",
    "lastname": "''' + last + '''",
    "firstname": "'''+first+'''",
    "sex": "f",
    "number": "15332",
    "type": "Régulier",
    "status": "'''+status+'''"
}'''
    
    data = json.loads(kwargs["data"])
    print(data)
    if data["physicianId"] == 12315332:
        return MockResponse("Annie", "Li", "Inscrit - Actif")
    if data["physicianId"] == 12300332:
        return MockResponse("Bobby", "Man", "Inscrit - Inactif")
    if data["physicianId"] == 12300000:
        return MockResponse("Annie", "Li", "")
    
    #Couldn't find given args
    assert False    

class TestGetStatus(unittest.TestCase):
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_verified(self, mock_get, mock_post):
        self.assertEqual(site10.get_status("Annie", "Li", "15332"), 'VERIFIED')
    
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_inactive(self, mock_get, mock_post):
        self.assertEqual(site10.get_status("Bobby", "Man", "332"), 'INACTIVE')

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_not_found(self, mock_get, mock_post):
        self.assertEqual(site10.get_status("Chad", "Chaderson", "0"), 'NOT FOUND')
    
if __name__ == '__main__':
    unittest.main()
