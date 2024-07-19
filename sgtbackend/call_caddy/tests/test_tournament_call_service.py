import os
import unittest
from unittest.mock import patch
import requests
import requests_mock
from datetime import datetime
from call_caddy.services.tournament_call import TournamentCallService

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
            f"https://live-golf-data.p.rapidapi.com/tournament?orgID=1&year={current_year}&tournId={tourn_id}",
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
            f"https://live-golf-data.p.rapidapi.com/tournament?orgID=1&year={current_year}&tournId={tourn_id}",
            status_code=404,
        )

        response = self.service.get_tournament("1", "475")
        self.assertIsNone(response)

    @requests_mock.Mocker()
    def test_get_schedule_connection_error(self, mocker):
        current_year = str(datetime.now().year)
        tourn_id = "475"
        mocker.get(
            f"https://live-golf-data.p.rapidapi.com/tournament?orgID=1&year={current_year}&tournId={tourn_id}",
            status_code=404,
        )

        response = self.service.get_tournament("1", "475")
        self.assertIsNone(response)