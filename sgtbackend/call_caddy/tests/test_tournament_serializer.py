from django.test import TestCase
from unittest.mock import patch, MagicMock
from call_caddy.serializers.tournament import TournamentSerializer
from call_caddy.helpers.evaluate_major_championship import is_major

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