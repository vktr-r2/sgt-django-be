from django.db import models
from django.utils import timezone


class Golfer(models.Model):
    source_id = models.CharField(max_length=10)
    f_name = models.CharField(max_length=16)
    l_name = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "golfer"

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Golfer, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.f_name} {self.l_name}"
