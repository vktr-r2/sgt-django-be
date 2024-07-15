from call_caddy.models.tournament import Tournament
from call_caddy.helpers.evaluate_major_championship import is_major

class TournamentDataProcessor:

    def __init__(self, validated_data):
        self.validated_data = validated_data

    def process_tournament_data(self):
        data = self.validated_data

        try:
            tournament_fields = {
                    "tournament_id": data["tournId"],
                    "year": int(data["year"]),
                    "source_id": data["_id"]["$oid"],
                    "golf_course": data["courses"][0]["courseName"],
                    "location": {
                        "city": data["courses"][0]["location"]["city"],
                        "state": data["courses"][0]["location"]["state"],
                        "country": data["courses"][0]["location"]["country"]
                        },
                    "par": int(data["courses"][0]["parTotal"]),
                    "time_zone": data["timeZone"],
                    "major_championship": is_major(data["name"])    # is_major helper function evaluates to bool
                }

            tournament = Tournament.objects.filter(tournament_id=tournament_fields["tournament_id"], year=tournament_fields["year"]).first()

            if tournament:
                # Update existing tournament
                for key, value in tournament_fields.items():
                    setattr(tournament, key, value)
                tournament.save()
            else:
                print(f"Tournament {tournament.source_id} did not exist in db.")

        except (KeyError, ValueError, TypeError) as e:
                print(f"Error processing tournament data: {e}")