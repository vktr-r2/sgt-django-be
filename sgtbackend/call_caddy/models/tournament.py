from django.db import models

class Tournament(models.Model):
    tournament_id = models.CharField(max_length=10, blank=True, default="")
    source_id = models.CharField(max_length=50, db_index=True)
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    golf_course = models.CharField(blank=True, max_length=100, default="")
    location = models.JSONField(null=True)
    par = models.IntegerField(null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    week_number = models.IntegerField()
    time_zone = models.CharField(max_length=20, blank=True, default="")
    format = models.CharField(max_length=20, default="stroke")
    major_championship = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tournament"
        indexes = [
            models.Index(fields=['tournament_id', 'year'], name='tournament_id_year_idx'),
        ]

    def __str__(self):
        return f"{self.name} ({self.year})"