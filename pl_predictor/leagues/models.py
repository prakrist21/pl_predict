from django.db import models
from django.conf import settings
# Create your models here.

class League(models.Model):
    name=models.CharField(max_length=100)
    host=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='leagues')
    invite_code=models.CharField(max_length=10,unique=True,blank=True)
    max_players=models.IntegerField(default=20)
    created_at=models.DateTimeField(auto_now_add=True)



class LeagueMember(models.Model):
    league=models.ForeignKey(League,on_delete=models.CASCADE,related_name="members")
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="memberships")
    joined_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=('league','user')

