from django.test import TestCase
from unittest.mock import patch, MagicMock
from call_caddy.serializers.schedule import ScheduleSerializer
from call_caddy.serializers.tournament import TournamentSerializer
from call_caddy.helpers.evaluate_major_championship import is_major

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
        self.assertTrue(serializer.is_valid())

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

class TournamentSerializerTest(TestCase):

    def setUp(self):
        self.valid_data= {
            "_id": {"$oid": "64fbe337235ac7657ff92842"},
            "courses": [{
                "courseName": "Pebble Beach",
                "location": {
                    "city": "Pebble Beach",
                    "state": "California",
                    "country": "USA"
                },
                "parTotal": "72",
            }],
            "timeZone": "PST",
            "major_championship": False
        }

    # Test data validation
    def test_tournament_serializer_is_valid(self):

        # Initialize serializer with data that needs to be validated
        serializer = TournamentSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    # Mock saving the data in a db
    @patch('call_caddy.serializers.tournament.TournamentSerializer.save', MagicMock(name="save"))
    def test_tournament_serializer_save(self):
        tournament_data = {
            "source_id": self.valid_data["_id"]["$oid"],
            "golf_course": self.valid_data["courses"][0]["courseName"],
            "location": {
                "city": self.valid_data["courses"][0]["location"]["city"],
                "state": self.valid_data["courses"][0]["location"]["state"],
                "country": self.valid_data["courses"][0]["location"]["country"]
                },
            "par": self.valid_data["courses"][0]["parTotal"],
            "time_zone": self.valid_data["timeZone"],
            "major_championship": self.valid_data["major_championship"]
        }

        # Initialize serializer with data that needs to be validated
        serializer = TournamentSerializer(data=tournament_data)
        serializer.save()
        
        #Ensure the save method was called once
        serializer.save.assert_called_once()
    
def test_is_major_is_a_major():
    assert is_major("Masters Tournament") == True
    assert is_major("PGA Championship") == True
    assert is_major("The Open Championship") == True
    assert is_major("U.S. Open") == True

def test_is_major_not_case_sensitive():
    assert is_major("MASTERS TOURNAMENT") == True
        
def test_is_major_is_not_a_major():
    assert is_major("Some random tourney") == False

def test_is_major_empty_string():
    assert is_major("") == False

def test_is_major_none():
    assert is_major(None) == False
