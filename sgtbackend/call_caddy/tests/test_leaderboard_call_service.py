import os
import unittest
from unittest.mock import patch
import requests_mock
from datetime import datetime
from call_caddy.services.leaderboard_call import LeaderboardCallService

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
            f"https://live-golf-data.p.rapidapi.com/leaderboard?orgID=1&year={current_year}&tournId={tourn_id}",
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
            f"https://live-golf-data.p.rapidapi.com/leaderboard?orgID=1&year={current_year}&tournId={tourn_id}",
            status_code=404,
        )

        response = self.service.get_leaderboard("1", "475")
        self.assertIsNone(response)

    @requests_mock.Mocker()
    def test_get_leaderboard_connection_error(self, mocker):
        current_year = str(datetime.now().year)
        tourn_id = "475"
        mocker.get(
            f"https://live-golf-data.p.rapidapi.com/leaderboard?orgID=1&year={current_year}&tournId={tourn_id}",
            status_code=404,
        )

        response = self.service.get_leaderboard("1", "475")
        self.assertIsNone(response)