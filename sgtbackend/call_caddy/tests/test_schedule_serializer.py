from django.test import TestCase
from unittest.mock import patch, MagicMock
from call_caddy.serializers.schedule import ScheduleSerializer


class ScheduleSerializerTest(TestCase):

    def setUp(self):
        self.valid_data = {
            "year": "2024",
            "schedule": [{
                "tournId": "1",
                "name": "Tournament 1",
                "date": {
                    "start": {
                        "$date": {
                            "$numberLong": "1719820800000"
                        }
                    },
                    "end": {
                        "$date": {
                            "$numberLong": "1720485599000"
                        }
                    },
                    "weekNumber": "27"
                },
                "format": "Stroke"
            }]         
        }

    # Test data validation
    def test_schedule_serializer_is_valid(self):

        # Initialize serializer with data that needs to be validated
        serializer = ScheduleSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), msg=serializer.errors)

    # Mock saving the data in a db
    @patch('call_caddy.serializers.schedule.ScheduleSerializer.save', MagicMock(name="save"))
    def test_schedule_serializer_save(self):
        tournament_data = {
            "tournament_id": self.valid_data["schedule"][0]["tournId"],
            "name": self.valid_data["schedule"][0]["name"],
            "year": self.valid_data["year"],
            "start_date": self.valid_data["schedule"][0]["date"]["start"]["$date"]["$numberLong"],
            "end_date": self.valid_data["schedule"][0]["date"]["end"]["$date"]["$numberLong"],
            "week_number": self.valid_data["schedule"][0]["date"]["weekNumber"],
            "format": self.valid_data["schedule"][0]["format"]
        }
        
        # Initialize serializer with data that needs to be saved
        serializer = ScheduleSerializer(tournament_data)
        serializer.save()

        # Ensure the save method was called once
        serializer.save.assert_called_once()