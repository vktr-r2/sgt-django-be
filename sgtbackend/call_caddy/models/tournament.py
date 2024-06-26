from django.db import models
from django.utils import timezone


class Tournament(models.Model):
    source_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    year = models.CharField(max_length=4)
    golf_course = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    par = models.IntegerField(null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    week_number = models.CharField(max_length=3)
    time_zone = models.CharField(max_length=20, null=True, blank=True)
    major_championship = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tournament"

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Tournament, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.year})"
