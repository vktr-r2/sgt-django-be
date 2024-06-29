from django.contrib import admin

# Register your models here.
from .models import Score, MatchResult

admin.site.register(Score)
admin.site.register(MatchResult)
