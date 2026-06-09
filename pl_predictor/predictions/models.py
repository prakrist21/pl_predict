from django.db import models
from django.conf import settings
# Create your models here.

class Gameweek(models.Model):
    number=models.IntegerField(unique=True,choices=[(x, f'GW {x}') for x in range(1, 39)])

    def __str__(self):
        return f"Gameweek {self.number}"


class Match(models.Model):
    gameweek=models.ForeignKey(Gameweek,on_delete=models.CASCADE,related_name="matches")
    home_team=models.CharField(max_length=100)
    away_team=models.CharField(max_length=100)
    kickoff_time=models.DateTimeField()
    home_score=models.IntegerField(null=True,blank=True)
    away_score=models.IntegerField(null=True,blank=True)
    status=models.CharField(max_length=20,default="SCHEDULED")
    match_id=models.IntegerField(unique=True)

class Prediction(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, related_name="predictions", on_delete=models.CASCADE)
    match=models.ForeignKey(Match,related_name="predictions", on_delete=models.CASCADE)
    pred_home=models.IntegerField(default=0)
    pred_away=models.IntegerField(default=0)
    points=models.IntegerField(default=0)
    submitted_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=('user','match')