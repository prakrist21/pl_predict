from django.forms import ModelForm
from .models import League
from django import forms

class LeagueForm(ModelForm):
    class Meta:
        model=League
        fields=["name"]

class JoinLeagueForm(forms.Form):
    invite_code=forms.CharField(max_length=10)