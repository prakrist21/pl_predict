from django import forms

class PredictionForm(forms.Form):
    pred_away=forms.IntegerField(min_value=0,max_value=100)
    pred_home=forms.IntegerField(min_value=0,max_value=100)