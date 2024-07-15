from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from datetime import datetime
import logging
from call_caddy.models.tournament import Tournament
from call_caddy.helpers.format_date import format_date

logger = logging.getLogger("call_caddy")

class ScheduleSerializer(serializers.ModelSerializer):
    year = serializers.CharField()
    schedule = serializers.ListField()

    class Meta:
        model = Tournament
        # /schedule endpoint gets just basics details of each tournament.  We get rest of tournament data from /tournament
        fields = ["schedule", "year"]

    def validate_year(self, value):
        if value != str(datetime.now().year):
            raise ValidationError("Year must be current year.")
        return value
    
    def validate_schedule(self, value):
        if len(value) == 0:
            raise ValidationError("Schedule list is empty")
        return value
    
    # custom validator function to iterate through schedule list of objects
    def validate(self, data):
        for tournament in data["schedule"]:
            start_date = format_date(tournament["date"]["start"]["$date"]["$numberLong"])
            end_date = format_date(tournament["date"]["end"]["$date"]["$numberLong"])

            try:
                if not isinstance(tournament["name"], str):
                    raise ValidationError("Name is not string format")
                if not isinstance(tournament["date"]["weekNumber"], str):
                    raise ValidationError("Week is not string format")
                if not isinstance(tournament["format"], str):
                    raise ValidationError("Format is not string format")
                if not isinstance(tournament["date"]["start"]["$date"]["$numberLong"], str):
                    raise ValidationError("Start date is not string format")
                if not isinstance(tournament["date"]["end"]["$date"]["$numberLong"], str):
                    raise ValidationError("End date is not string format")
                if end_date < start_date:
                    raise ValidationError("Start date is not before end date")
            except ValidationError as e:
                print(f"Validation error: {e}")
                logger.error(f"Validation error: {e}")
                raise e
        return data