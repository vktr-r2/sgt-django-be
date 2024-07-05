from rest_framework import serializers
from models import Tournament
from django.utils.dateparse import parse_datetime

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ["source_id", "name", "year", "start_date", "end_date", "week_number", "format"]   # These are the only fields we need from /schedule endpoint

def insert_schedule_data(response):
    for tournament_data in response.get("schedule", []):    #"schedule" value is a list of tournament objects in the JSON response
        tournament = {
            "source_id": tournament_data["tournId"],
            "name": tournament_data["name"],
            "year": response["year"],
            "start_date": parse_datetime(tournament_data["date"]["start"]),
            "end_date": parse_datetime(tournament_data["date"]["end"]),
            "week_number": tournament_data["date"]["weekNumber"],
            "format": tournament_data["format"]
        }

        serializer = ScheduleSerializer(data=tournament)
        if serializer.is_valid():
            serializer.save()
        else:
            print(f"Error saving tournament {tournament_data["name"]}: {serializer.errors}")
