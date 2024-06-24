import os
import unittest
from unittest.mock import patch
import requests
import requests_mock
from call_caddy.services.rapid_api_wrapper import RapidApiWrapperService

class TestRapidApiWrapperService(unittest.TestCase):

    # Setup wrapper with patched authentication for each test
    @patch.dict(os.environ, {"RAPID_API_KEY": "fake_api_key"})
    def setUp(self):
        self.service = RapidApiWrapperService()


    @requests_mock.Mocker()
    def test_make_request_success(self, mocker):
        # Mock request 200
        mocker.get("https://live-golf-data.p.rapidapi.com/mock-endpoint", json={"key":"value"}, status_code=200)

        # Call make_request method with "mock-endpoint" URL path
        response = self.service.make_request("mock-endpoint")

        self.assertIsNotNone(response) # Check we got a response
        self.assertEqual(response, {"key": "value"}) # Check response is as expected


    @requests_mock.Mocker()
    def test_make_request_http_error(self, mocker):
        # Mock request 404
        mocker.get("https://live-golf-data.p.rapidapi.com/mock-endpoint", status_code=404)
        
        # Call make_request method
        response = self.service.make_request("mock_endpoint")
        
        # Assert response is None
        self.assertIsNone(response)


    @requests_mock.Mocker()
    def test_make_request_connection_error(self, mocker):
        # Mock ConnectionError
        mocker.get("https://live-golf-data.p.rapidapi.com/mock-endpoint", exc=requests.ConnectionError)
        
        # Call make_request
        response = self.service.make_request("mock_endpoint")
        
        self.assertIsNone(response)


    @requests_mock.Mocker()
    def test_make_request_timeout(self, mocker):
        # Mock Timeout
        mocker.get("https://live-golf-data.p.rapidapi.com/mock-endpoint", exc=requests.Timeout)
        
        # Call make_request
        response = self.service.make_request("mock_endpoint")
        
        self.assertIsNone(response)


    @requests_mock.Mocker()
    def test_make_request_generic_exception(self, mocker):
        # Mock generic Exception
        mocker.get("https://live-golf-data.p.rapidapi.com/mock-endpoint", exc=Exception)
        
        # Call make_request
        response = self.service.make_request("mock_endpoint")
        
        self.assertIsNone(response)


if __name__ == "__main__":
    unittest.main()