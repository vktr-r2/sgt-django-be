from django.db import models
from django.utils import timezone


class Golfer(models.Model):
    source_id = models.CharField(max_length=50, db_index=True)
    f_name = models.CharField(max_length=32)
    l_name = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "golfer"

    def __str__(self):
        return f"{self.f_name} {self.l_name}"
