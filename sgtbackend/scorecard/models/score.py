from django.db import models
from django.utils import timezone
from rough_draft.models import MatchPick


class Score(models.Model):
    match_picks_id = models.ForeignKey(MatchPick, on_delete=models.CASCADE, db_index=True)
    score = models.IntegerField(null=True, blank=True)
    round = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'score'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Score, self).save(*args, **kwargs)

    def __str__(self):
        return f"Score {self.id}: {self.score} for round {self.round}"
