from rest_framework import serializers
from models import Tournament
from call_caddy.helpers.evaluate_major_championship import is_major


class TournamentSerializer(serializers.ModelSerializer):
    golf_course = serializers.CharField()
    location = serializers.JSONField()
    par = serializers.IntegerField()
    time_zone = serializers.CharField()
    major_championship = serializers.BooleanField()
    
    class Meta:
        model = Tournament
        fields = ["golf_course", "location", "par", "time_zone", "major_championship"]  # These are the only fields we need from /tournament endpoint

def put_tournament_details_data(response):
        tournament_details = {
            "golf_course": response["course"][0]["courseName"],
            "location": {
                "city": response["course"][0]["location"]["city"],
                "state": response["course"][0]["location"]["state"],
                "country": response["course"][0]["location"]["country"]
                },
            "par": int(response["course"][0]["parTotal"]),
            "time_zone": response["timeZone"],
            "major_championship": is_major(response["name"])    # is_major helper function evaluates to bool
        }

        serializer = TournamentSerializer(data=tournament_details)
        if serializer.is_valid():
            serializer.save()
        else:
            print(f"Error saving tournament details {tournament_details["name"]}: {serializer.errors}")






"""
THIS NEEDS TO LIVE ELSEWHERE IN THE CODE
import TournamentCallService
import TournamentSerializer


tournaments_list = create_tournaments_list()

for tournament in tournaments_list:
    tournament_data = TournamentCallService("1", tournament)
    put_tournament_data(tournament_data)


    golf_course = models.CharField(blank=True, max_length=100, default="")
    location = models.CharField(blank=True, max_length=255, default="")
    par = models.IntegerField(null=True)
    time_zone = models.CharField(max_length=20, blank=True, default="")
    major_championship = models.BooleanField(default=False)

    

"""