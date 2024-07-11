from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import datetime
from call_caddy.models.tournament import Tournament

class ScheduleSerializer(serializers.ModelSerializer):
    tournament_id = serializers.CharField()
    name = serializers.CharField()
    year = serializers.IntegerField()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    week_number = serializers.IntegerField()
    format = serializers.CharField()

    class Meta:
        model = Tournament
        # These are the only fields we need from /schedule endpoint, rest will be imported from /tournament 
        fields = ["tournament_id", "name", "year", "start_date", "end_date", "week_number", "format"]

    def validate_year(self, value):
        if value <= 2018:
            raise ValidationError("Year must be after 2018.")
        return value
    
    def validate_week_number(self, value):
        if value >= 53:
            raise ValidationError("Week number cannot exceed 52")
        return value

    def validate(self, data):
        if data['start_date'] >= data['end_date']:
            raise ValidationError("End date must be after start date.")
        return data


    @staticmethod
    def insert_schedule_data(response):
        for tournament_data in response.get("schedule", []):    #"schedule" value is a list of tournament objects in the JSON response
        

            try:
                start_date_ms = int(tournament_data["date"]["start"]["$date"]["$numberLong"])
                end_date_ms = int(tournament_data["date"]["end"]["$date"]["$numberLong"])

                 # Convert milliseconds to seconds
                start_date = datetime.datetime.fromtimestamp(start_date_ms / 1000)
                end_date = datetime.datetime.fromtimestamp(end_date_ms / 1000)

                tournament = {
                    "tournament_id": tournament_data["tournId"],
                    "name": tournament_data["name"],
                    "year": int((response["year"])),
                    "start_date": start_date,
                    "end_date": end_date,
                    "week_number": tournament_data["date"]["weekNumber"],
                    "format": tournament_data["format"]
                }

                # Checks if tournament is already in db or not
                if Tournament.objects.filter(tournament_id=tournament_data["tournId"], year=int((response["year"]))):
                    print(f"Tournament {tournament_data["tournId"]} for year {response["year"]} already exists.")
                else:
                    # If tournament not in db, validate data and save tournament
                    serializer = ScheduleSerializer(data=tournament)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        print(f"Error saving tournament {tournament_data["name"]}: {serializer.errors}")

            except (KeyError, ValueError, TypeError) as e:
                print(f"Error processing tournament data: {e}")