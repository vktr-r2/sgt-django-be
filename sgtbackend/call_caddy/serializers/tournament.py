from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from call_caddy.models import Tournament
from call_caddy.helpers.evaluate_major_championship import is_major


class TournamentSerializer(serializers.ModelSerializer):
    source_id = serializers.CharField()
    golf_course = serializers.CharField()
    location = serializers.JSONField()
    par = serializers.IntegerField()
    time_zone = serializers.CharField()
    major_championship = serializers.BooleanField()

    class Meta:
        model = Tournament
        fields = ["source_id", "golf_course", "location", "par", "time_zone", "major_championship"]  # These are the only fields we need from /tournament endpoint

    def validate_par(self, value):
        if value <= 69 or value >= 73:
            raise ValidationError("Year must be after 2018.")
        return value
    
    @staticmethod
    def put_tournament_details_data(response):
            try:
                tournament_details = {
                    "source_id": response["_id"],
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
            
            except (KeyError, ValueError, TypeError) as e:
                print(f"Error processing tournament data: {e}")





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