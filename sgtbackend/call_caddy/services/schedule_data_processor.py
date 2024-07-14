import datetime
from call_caddy.models.tournament import Tournament
from call_caddy.serializers.schedule import ScheduleSerializer
from call_caddy.helpers.format_date import format_date


class ScheduleDataProcessor:

    def __init__(self, validated_data):
        self.validated_data = validated_data

    def process_schedule_data(self):
        for tournament_data in self.validated_data.get("schedule", []):    #"schedule" value is a list of tournament objects in the JSON response
        
            try:
                # Convert string to datetime object
                start_date = format_date(tournament_data["date"]["start"]["$date"]["$numberLong"])
                end_date = format_date(tournament_data["date"]["end"]["$date"]["$numberLong"])

                tournament = {
                    "tournament_id": tournament_data["tournId"],
                    "name": tournament_data["name"],
                    "year": int(self.validated_data["year"]),
                    "start_date": start_date,
                    "end_date": end_date,
                    "week_number": tournament_data["date"]["weekNumber"],
                    "format": tournament_data["format"]
                }

                # Filter by tournId and year to check if tournament object is already in db or not
                if Tournament.objects.filter(tournament_id=tournament["tournament_id"], year=tournament["year"]).exists():
                    print(f"Tournament {tournament['tournament_id']} for year {tournament['year']} already exists.")
                else:
                    # Save the tournament to the database
                    Tournament.objects.create(**tournament)
                    print(f"Tournament {tournament['name']} saved successfully.")

            except (KeyError, ValueError, TypeError) as e:
                print(f"Error processing tournament data: {e}")