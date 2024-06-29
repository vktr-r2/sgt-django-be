from django.db import models
from django.utils import timezone
from call_caddy.models import Tournament, Golfer
from grounds_crew.models import User


class MatchPick(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="match_pick")
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="match_pick")
    golfer = models.ForeignKey(Golfer, on_delete=models.CASCADE, related_name="match_pick")
    priority = models.IntegerField()
    drafted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "match_pick"

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(MatchPick, self).save(*args, **kwargs)

    def __str__(self):
        return f"MatchPick({self.user}, {self.tournament}, {self.golfer}, {self.priority})"
