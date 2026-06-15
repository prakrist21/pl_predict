from django.shortcuts import render, redirect
from .models import Gameweek,Match, Prediction
from django.utils import timezone
from .forms import PredictionForm
# Create your views here.


def gameweek_list(request):
    gameweek=Gameweek.objects.all()
    return render(request,"predictions/gameweek_list.html",{"gameweek":gameweek})

def gameweek_detail(request,gw_number):
    gameweek=Gameweek.objects.get(number=gw_number)
    matches=Match.objects.filter(gameweek=gameweek)

    user_predictions={}
    if request.user.is_authenticated:
        predictions=Prediction.objects.filter(
            user=request.user,
            match__in=matches
        )
        user_predictions={p.match_id: p for p in predictions}

    match_data=[]
    for match in matches:
        match_data.append({
            'match':match,
            'user_prediction':user_predictions.get(match.match_id)
        })

    return render(request,"predictions/gameweek_detail.html",{"match_data":match_data,"gameweek":gameweek})

def submit_prediction(request, match_id):
    match=Match.objects.get(match_id=match_id)

    # if timezone.now() >= match.kickoff_time:
    #     return redirect("gameweek_detail",gw_number=match.gameweek.number)
    
    prediction=Prediction.objects.filter(user=request.user, match=match).first()

    if request.method=="POST":
        form=PredictionForm(request.POST)

        if form.is_valid():
            
            pred_home=form.cleaned_data["pred_home"]
            pred_away=form.cleaned_data["pred_away"]
            if prediction:
                prediction.pred_home=pred_home
                prediction.pred_away=pred_away
                prediction.save()
            else:
                Prediction.objects.create(
                    user=request.user,
                    match=match,
                    pred_away=pred_away,
                    pred_home=pred_home
                )

            return redirect("gameweek_detail",gw_number=match.gameweek.number)


    else:
        if prediction:
            form = PredictionForm(initial={
                'pred_home': prediction.pred_home,
                'pred_away': prediction.pred_away
            })
        else:
            form = PredictionForm()

    return render(request,"predictions/submit_prediction.html",{"form":form,"match":match})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.management import call_command
import os

@csrf_exempt
def trigger_fetch_results(request):
    if request.method == 'POST':
        secret = request.headers.get('X-Secret-Key')
        if secret != os.getenv('CRON_SECRET'):
            return JsonResponse({'error': 'unauthorized'}, status=401)
        call_command('fetch_results')
        return JsonResponse({'status': 'done'})