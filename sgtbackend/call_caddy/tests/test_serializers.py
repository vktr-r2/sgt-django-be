from django.test import TestCase
from rest_framework.exceptions import ValidationError
from django.utils.dateparse import parse_datetime
from unittest.mock import patch, MagicMock
from call_caddy.serializers.schedule import ScheduleSerializer
from call_caddy.serializers.tournament import TournamentSerializer

class ScheduleSerializerTest(TestCase):

    def setUp(self):
        self.valid_data = {
            "tournId": "1",
            "name": "Tournament 1",
            "date": {
                "start": "2024-07-01T00:00:00Z",
                "end": "2024-07-07T23:59:59Z",
                "weekNumber": 27
            },
            "format": "Stroke"
        }
        self.response_data = {
            "year": 2024,
            "schedule": [self.valid_data]
        }

    def test_schedule_serializer_is_valid(self):
        tournament_data = {
            "source_id": self.valid_data["tournId"],
            "name": self.valid_data["name"],
            "year": self.response_data["year"],
            "start_date": parse_datetime(self.valid_data["date"]["start"]),
            "end_date": parse_datetime(self.valid_data["date"]["end"]),
            "week_number": self.valid_data["date"]["weekNumber"],
            "format": self.valid_data["format"]
        }

        serializer = ScheduleSerializer(data=tournament_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['source_id'], self.valid_data['tournId'])
        self.assertEqual(serializer.validated_data['name'], self.valid_data['name'])
        self.assertEqual(serializer.validated_data['year'], self.response_data['year'])
        self.assertEqual(serializer.validated_data['start_date'], parse_datetime(self.valid_data['date']['start']))
        self.assertEqual(serializer.validated_data['end_date'], parse_datetime(self.valid_data['date']['end']))
        self.assertEqual(serializer.validated_data['week_number'], self.valid_data['date']['weekNumber'])
        self.assertEqual(serializer.validated_data['format'], self.valid_data['format'])

    @patch('call_caddy.serializers.schedule.ScheduleSerializer.save', MagicMock(name="save"))
    def test_schedule_serializer_save(self):
        tournament_data = {
            "source_id": self.valid_data["tournId"],
            "name": self.valid_data["name"],
            "year": self.response_data["year"],
            "start_date": parse_datetime(self.valid_data["date"]["start"]),
            "end_date": parse_datetime(self.valid_data["date"]["end"]),
            "week_number": self.valid_data["date"]["weekNumber"],
            "format": self.valid_data["format"]
        }

        serializer = ScheduleSerializer(data=tournament_data)
        if serializer.is_valid():
            serializer.save()
        else:
            self.fail(f"Serializer failed: {serializer.errors}")

        # Ensure the save method was called once
        serializer.save.assert_called_once()

class TournamentSerializerTest(TestCase):

    def setUp(self):
        self.valid_data= {
            "course": [{
                "courseName": "Pebble Beach",
                "location": {
                    "city": "Pebble Beach",
                    "state": "California",
                    "country": "USA"
                }
            }],
            "par": 72,
            "time_zone": "PST",
            "major_championship": False
        }

    def test_tournament_serializer_is_valid(self):
        tournament_data = {
            "golf_course": self.valid_data["course"][0]["courseName"],
            "location": {
                "city": self.valid_data["course"][0]["location"]["city"],
                "state": self.valid_data["course"][0]["location"]["state"],
                "country": self.valid_data["course"][0]["location"]["country"]
                },
            "par": self.valid_data["par"],
            "time_zone": self.valid_data["time_zone"],
            "major_championship": self.valid_data["major_championship"]
        }

        serializer = TournamentSerializer(data=tournament_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["golf_course"], self.valid_data["course"][0]["courseName"])
        self.assertEqual(serializer.validated_data["location"]["city"], self.valid_data["course"][0]["location"]["city"])
        self.assertEqual(serializer.validated_data["location"]["state"], self.valid_data["course"][0]["location"]["state"])
        self.assertEqual(serializer.validated_data["location"]["country"], self.valid_data["course"][0]["location"]["country"])
        self.assertEqual(serializer.validated_data["par"], self.valid_data["par"])
        self.assertEqual(serializer.validated_data["time_zone"], self.valid_data["time_zone"])
        self.assertEqual(serializer.validated_data["major_championship"], self.valid_data["major_championship"])

    @patch('call_caddy.serializers.tournament.TournamentSerializer.save', MagicMock(name="save"))
    def test_tournament_serializer_save(self):
        tournament_data = {
            "golf_course": self.valid_data["course"][0]["courseName"],
            "location": {
                "city": self.valid_data["course"][0]["location"]["city"],
                "state": self.valid_data["course"][0]["location"]["state"],
                "country": self.valid_data["course"][0]["location"]["country"]
                },
            "par": self.valid_data["par"],
            "time_zone": self.valid_data["time_zone"],
            "major_championship": self.valid_data["major_championship"]
        }

        serializer = TournamentSerializer(data=tournament_data)
        if serializer.is_valid():
            serializer.save()
        else:
            self.fail(f"Serializer failed: {serializer.errors}")

        #Ensure the save method was called once
        serializer.save.assert_called_once()