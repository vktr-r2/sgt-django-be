import os
import unittest
from unittest.mock import patch
import requests
import requests_mock
from datetime import datetime
from call_caddy.services.rapid_api_wrapper import RapidApiWrapperService
from call_caddy.services.schedule_call import ScheduleCallService
from call_caddy.services.tournament_call import TournamentCallService
from call_caddy.services.leaderboard_call import LeaderboardCallService


class TestRapidApiWrapperService(unittest.TestCase):

    # Setup wrapper with patched authentication for each test
    @patch.dict(os.environ, {"RAPID_API_KEY": "fake_api_key"})
    def setUp(self):
        self.service = RapidApiWrapperService()

    @requests_mock.Mocker()
    def test_make_request_success(self, mocker):
        # Mock request 200
        mocker.get("https://live-golf-data.p.rapidapi.com/mock-endpoint", json={"key": "value"}, status_code=200)

        # Call make_request method with "mock-endpoint" URL path
        response = self.service.make_request("mock-endpoint")

        self.assertIsNotNone(response)  # Check we got a response
        self.assertEqual(response, {"key": "value"})  # Check response is as expected

    @requests_mock.Mocker()
    def test_make_request_http_error(self, mocker):
        # Mock request 404
        mocker.get("https://live-golf-data.p.rapidapi.com/mock-endpoint", status_code=404)

        # Call make_request method
        response = self.service.make_request("mock-endpoint")

        # Assert response is None
        self.assertIsNone(response)

    @requests_mock.Mocker()
    def test_make_request_connection_error(self, mocker):
        # Mock ConnectionError
        mocker.get("https://live-golf-data.p.rapidapi.com/mock-endpoint", exc=requests.ConnectionError)

        # Call make_request
        response = self.service.make_request("mock-endpoint")

        self.assertIsNone(response)

    @requests_mock.Mocker()
    def test_make_request_timeout(self, mocker):
        # Mock Timeout
        mocker.get("https://live-golf-data.p.rapidapi.com/mock-endpoint", exc=requests.Timeout)

        # Call make_request
        response = self.service.make_request("mock-endpoint")

        self.assertIsNone(response)

    @requests_mock.Mocker()
    def test_make_request_generic_exception(self, mocker):
        # Mock generic Exception
        mocker.get("https://live-golf-data.p.rapidapi.com/mock-endpoint", exc=Exception)

        # Call make_request
        response = self.service.make_request("mock-endpoint")

        self.assertIsNone(response)


#################################################################


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


#################################################################


class TestTournamentCallService(unittest.TestCase):

    @patch.dict(os.environ, {"RAPID_API_KEY": "fake_api_key"})
    def setUp(self):
        self.service = TournamentCallService()

    @requests_mock.Mocker()
    def test_get_tournament(self, mocker):
        current_year = str(datetime.now().year)
        tourn_id = "475"
        mock_tourney = {
            "_id": "64fbe447235ac8857ff92842",
            "orgId": "1",
            "year": "2024",
            "tournId": "475",
            "name": "Valspar Championship",
            "date": {"start": "2024-03-21T00:00:00Z", "end": "2024-03-24T00:00:00Z", "weekNumber": "12"},
            "format": "stroke",
            "status": "Official",
            "timeZone": "America/New_York",
        }

        # Mock successful tourney GET
        mocker.get(
            f"https://live-golf-data.p.rapidapi.com/tournament?orgID=1&year={current_year}&tourn_id={tourn_id}",
            json=mock_tourney,
            status_code=200,
        )
        # Call get_tournament
        response = self.service.get_tournament("1", "475")

        # Assert
        self.assertIsNotNone(response)
        self.assertEqual(response, mock_tourney)

    @requests_mock.Mocker()
    def test_get_schedule_http_error(self, mocker):
        current_year = str(datetime.now().year)
        tourn_id = "475"
        mocker.get(
            f"https://live-golf-data.p.rapidapi.com/tournament?orgID=1&year={current_year}&tourn_id={tourn_id}",
            status_code=404,
        )

        response = self.service.get_tournament("1", "475")
        self.assertIsNone(response)

    @requests_mock.Mocker()
    def test_get_schedule_connection_error(self, mocker):
        current_year = str(datetime.now().year)
        tourn_id = "475"
        mocker.get(
            f"https://live-golf-data.p.rapidapi.com/tournament?orgID=1&year={current_year}&tourn_id={tourn_id}",
            status_code=404,
        )

        response = self.service.get_tournament("1", "475")
        self.assertIsNone(response)


#################################################################


class TestLeaderboardCallService(unittest.TestCase):

    @patch.dict(os.environ, {"RAPID_API_KEY": "fake_api_key"})
    def setUp(self):
        self.service = LeaderboardCallService()

    @requests_mock.Mocker()
    def test_get_leaderboard(self, mocker):
        current_year = str(datetime.now().year)
        tourn_id = "475"
        mock_leaderboard = {
            "_id": "667c23756b50b272b2919df9",
            "orgId": "1",
            "year": "2024",
            "tournId": "524",
            "status": "In Progress",
            "roundId": "1",
            "roundStatus": "Official",
            "lastUpdated": "2024-06-27T23:21:23.382Z",
            "timestamp": "2024-06-27T23:21:23.382Z",
        }

        # Mock successful tourney GET
        mocker.get(
            f"https://live-golf-data.p.rapidapi.com/leaderboard?orgID=1&year={current_year}&tourn_id={tourn_id}",
            json=mock_leaderboard,
            status_code=200,
        )
        # Call get_tournament
        response = self.service.get_leaderboard("1", "475")

        # Assert
        self.assertIsNotNone(response)
        self.assertEqual(response, mock_leaderboard)

    @requests_mock.Mocker()
    def test_get_leaderboard_http_error(self, mocker):
        current_year = str(datetime.now().year)
        tourn_id = "475"
        mocker.get(
            f"https://live-golf-data.p.rapidapi.com/leaderboard?orgID=1&year={current_year}&tourn_id={tourn_id}",
            status_code=404,
        )

        response = self.service.get_leaderboard("1", "475")
        self.assertIsNone(response)

    @requests_mock.Mocker()
    def test_get_leaderboard_connection_error(self, mocker):
        current_year = str(datetime.now().year)
        tourn_id = "475"
        mocker.get(
            f"https://live-golf-data.p.rapidapi.com/leaderboard?orgID=1&year={current_year}&tourn_id={tourn_id}",
            status_code=404,
        )

        response = self.service.get_leaderboard("1", "475")
        self.assertIsNone(response)


if __name__ == "__main__":
    unittest.main()
