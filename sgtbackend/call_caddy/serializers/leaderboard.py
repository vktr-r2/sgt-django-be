from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from datetime import datetime
import logging
from scorecard.models.score import Score
from call_caddy.helpers.format_date import format_date

logger = logging.getLogger("call_caddy")

class RoundsSerializer(serializers.Serializer):
    scoreToPar = serializers.CharField()
    roundId = serializers.DictField()
    strokes = serializers.DictField()

    class Meta:
        fields = ["scoreToPar", "roundId", "strokes"]

class LeaderboardRowSerializer(serializers.Serializer):
    lastName = serializers.CharField()
    firstName = serializers.CharField()
    playerId = serializers.CharField()
    status = serializers.CharField()
    position = serializers.CharField()
    total = serializers.CharField()
    currentRoundScore = serializers.CharField()
    totalStrokesFromCompletedRounds = serializers.CharField()
    currentHole = serializers.DictField()
    roundComplete = serializers.BooleanField()
    rounds = serializers.ListField(child = RoundsSerializer())
    thru = serializers.CharField()
    currentRound = serializers.DictField()

    class Meta:
        fields = ["lastName", "firstName", "playerId", "status", "position", "total", "currentRoundScore", "totalStrokesFromCompletedRounds", "roundComplete"]

class LeaderboardSerializer(serializers.Serializer):
    status = serializers.CharField()
    roundId = serializers.DictField()
    roundStatus = serializers.CharField()
    cutLines = serializers.ListField()
    leaderboardRows = serializers.ListField(child=LeaderboardRowSerializer())

    class Meta:
        fields = ["status", "roundId", "roundStatus", "cutLines", "leaderboardRows"]



