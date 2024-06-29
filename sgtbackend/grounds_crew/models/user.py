from django.db import models
import uuid
from django.utils import timezone


class User(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(max_length=40, unique=True)
    username = models.CharField(max_length=16, unique=True)
    password = models.CharField(max_length=255)
    f_name = models.CharField(max_length=16)
    l_name = models.CharField(max_length=16)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "user"

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username
