import os
import unittest
from unittest.mock import patch
import requests
import requests_mock
from datetime import datetime
from call_caddy.services.schedule_call import ScheduleCallService

class TestScheduleCallService(unittest.TestCase):

    @patch.dict(os.environ, {"RAPID_API_KEY": "fake_api_key"})
    def setUp(self):
        self.service = ScheduleCallService()

    @requests_mock.Mocker()
    def test_get_schedule(self, mocker):
        current_year = str(datetime.now().year)
        mock_schedule = {
            "org_id": "1",
            "year": current_year,
            "events": [
                {"The Masters": "Event 1", "date": f"{current_year}-01-01"},
                {"PGA Championship": "Event 2", "date": f"{current_year}-02-01"},
            ],
        }

        # Mock successful schedule GET
        mocker.get(
            f"https://live-golf-data.p.rapidapi.com/schedule?orgID=1&year={current_year}",
            json=mock_schedule,
            status_code=200,
        )

        # Call get_schedule
        response = self.service.get_schedule("1")

        # Asset current years schedule is returned
        self.assertIsNotNone(response)
        self.assertEqual(response, mock_schedule)
        self.assertEqual(response["year"], current_year)
        for event in response["events"]:
            self.assertTrue(event["date"].startswith(current_year))

    @requests_mock.Mocker()
    def test_get_schedule_http_error(self, mocker):
        current_year = str(datetime.now().year)
        mocker.get(f"https://live-golf-data.p.rapidapi.com/schedule?orgID=1&year={current_year}", status_code=404)

        response = self.service.get_schedule("1")
        self.assertIsNone(response)

    @requests_mock.Mocker()
    def test_get_schedule_connection_error(self, mocker):
        current_year = str(datetime.now().year)
        mocker.get(
            f"https://live-golf-data.p.rapidapi.com/schedule?orgID=1&year={current_year}", exc=requests.ConnectionError
        )

        response = self.service.get_schedule("1")
        self.assertIsNone(response)