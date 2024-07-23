from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import logging

logger = logging.getLogger("call_caddy")

class PlayerSerializer(serializers.Serializer):
    lastName = serializers.CharField()
    firstName = serializers.CharField()
    playerId = serializers.CharField()

    class Meta:
        # players is a list returned from the /tournament response
        fields = ["lastName", "firstName", "playerId"]
    
    def validate(self, data):
        try:
            if not isinstance(data["lastName"], str):
                raise ValidationError("lastName is not in string format")
            if not isinstance(data["firstName"], str):
                raise ValidationError("firstName is not in string format")
            if not isinstance(data["playerId"], str):
                raise ValidationError("playerId is not in string format")

        except ValidationError as e:
            print(f"Validation error: {e}")
            logger.error(f"Validation error: {e}")
            raise e
        return data

class TournamentSerializer(serializers.Serializer):
    _id = serializers.DictField()
    courses = serializers.ListField()
    timeZone = serializers.CharField()
    players = serializers.ListField(child = PlayerSerializer())


    class Meta:
        # /tournament endpoint returns tournament details and players, rest of tournament data should already be imported from /schedule
        fields = ["_id", "courses", "timeZone", "players"]

    # custom validator
    def validate(self, data):
        try:
            if not isinstance(data["_id"], dict):
                raise ValidationError("_id is not in dict format")
            if not isinstance(data["courses"][0]["courseName"], str):
                raise ValidationError("courseName is not string format")
            if not isinstance(data["courses"][0]["location"]["city"], str):
                raise ValidationError("City is not string format")
            if not isinstance(data["courses"][0]["location"]["state"], str) and data["courses"][0]["location"]["state"] != None:
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


    