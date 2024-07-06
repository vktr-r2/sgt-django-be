from django.test import TestCase
from rest_framework.exceptions import ValidationError
from django.utils.dateparse import parse_datetime
from unittest.mock import patch, MagicMock
from call_caddy.serializers.schedule import ScheduleSerializer

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