from django.contrib import admin
from .models import Gameweek, Match, Prediction

admin.site.register(Gameweek)
admin.site.register(Match)
admin.site.register(Prediction)
