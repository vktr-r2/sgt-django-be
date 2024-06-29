from django.db import models
from django.utils import timezone
from call_caddy.models import Tournament
from grounds_crew.models import User


class MatchResult(models.Model):
    tournament_id = models.ForeignKey(Tournament, on_delete=models.CASCADE, db_index=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    total_score = models.IntegerField()
    place = models.IntegerField()
    winner_picked = models.BooleanField(default=False)
    cuts_missed = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "match_result"

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(MatchResult, self).save(*args, **kwargs)

    def __str__(self):
        return f"Match Result {self.id}: User {self.user_id} in Tournament {self.tournament_id}"
