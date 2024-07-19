from django.test import TestCase
from call_caddy.serializers.leaderboard import LeaderboardSerializer


class LeaderboardSerializerTest(TestCase):

    def setUp(self):
        self.valid_data = {
            "status": "In Progress",
            "roundId": {"$numberInt": "1"},
            "roundStatus": "Official",
            "cutLines": [],
            "leaderboardRows": [{
                "lastName": "Brown", 
                "firstName": "Daniel", 
                "playerId": "57259", 
                "status": "complete", 
                "position": "1", 
                "total": "-6", 
                "currentRoundScore": "-6", 
                "totalStrokesFromCompletedRounds": "65", 
                "currentHole": {
                    "$numberInt": "18"
                    }, 
                "roundComplete": True, 
                "rounds": [{
                    "scoreToPar": "-6", 
                    "roundId": {
                        "$numberInt": "1"
                        }, 
                    "strokes": {
                        "$numberInt": "65"
                        }
                    }], 
                "thru": "F", 
                "currentRound": {
                    "$numberInt": "1"
                    }, 
                "teeTime": "4:16pm", 
                "teeTimeTimestamp": {
                    "$date": {"$numberLong": "1721315760000"}
                    }
                }],      
        }

    # Test data validation
    def test_leaderboard_serializer_is_valid(self):

        # Initialize serializer with data that needs to be validated
        serializer = LeaderboardSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    """# Mock saving the data in a db
    @patch("call_caddy.serializers.schedule.ScheduleSerializer.save", MagicMock(name="save"))
    def test_leaderboard_serializer_save(self):
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
        serializer = LeaderboardSerializer(tournament_data)
        serializer.save()

        # Ensure the save method was called once
        serializer.save.assert_called_once()"""
