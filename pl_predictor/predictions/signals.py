from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Match, Prediction

@receiver(post_save, sender=Match)
def calculate_points(sender, instance, **kwargs):
    match=instance
    if match.status != 'FINISHED':
        return

    predictions=Prediction.objects.filter(match=match)

    for prediction in predictions:
        pred_home=prediction.pred_home
        pred_away=prediction.pred_away
        actual_home=match.home_score
        actual_away=match.away_score 

        if pred_home == actual_home and pred_away == actual_away:
            prediction.points = 3
        elif (pred_home - pred_away) == (actual_home - actual_away):
            prediction.points = 2
        elif (pred_home > pred_away) == (actual_home > actual_away):
            prediction.points = 1
        else:
            prediction.points = 0
        
        prediction.save()
    