from django.db import models
from django.utils import timezone
from rough_picks.models import MatchPick


class Score(models.Model):
    match_picks_id = models.ForeignKey(MatchPick, on_delete=models.CASCADE, db_index=True)
    score = models.IntegerField(null=True, blank=True)
    round = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     db_table = 'score'
    #     indexes = [
    #         models.Index(fields=['match_pick_id']),
    #     ]

    def __str__(self):
        return f"Score {self.id}: {self.score} for round {self.round}"
