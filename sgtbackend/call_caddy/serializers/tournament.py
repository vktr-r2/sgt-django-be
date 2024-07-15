from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import logging
from call_caddy.models import Tournament

logger = logging.getLogger("call_caddy")

class TournamentSerializer(serializers.ModelSerializer):
    _id = serializers.DictField()
    courses = serializers.ListField()
    timeZone = serializers.CharField()

    class Meta:
        model = Tournament
        # /tournament endpoint returns tournament details, rest of tournament data should already be imported from /schedule
        fields = ["_id", "courses", "timeZone"]

    # custom validator
    def validate(self, data):
        try:
            if not isinstance(data["_id"], str):
                raise ValidationError("_id is not in dict format")
            if not isinstance(data["courses"][0]["courseName"], str):
                raise ValidationError("courseName is not string format")
            if not isinstance(data["courses"][0]["location"]["city"], str):
                raise ValidationError("City is not string format")
            if not isinstance(data["courses"][0]["location"]["state"], str):
                raise ValidationError("State is not string format")
            if not isinstance(data["courses"][0]["location"]["country"], str):
                raise ValidationError("Country is not string format")
            if not isinstance(data["courses"][0]["parTotal"], str):
                raise ValidationError("Par is not string format")
            if not isinstance(data["timeZone"], str):
                raise ValidationError("Time zone is not string format")
        except ValidationError as e:
            print(f"Validation error: {e}")
            logger.error(f"Validation error: {e}")
            raise e
        return data