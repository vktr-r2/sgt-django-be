from django.contrib import admin

# Register your models here.
from .models import Tournament, Golfer

admin.site.register(Tournament)
admin.site.register(Golfer)
