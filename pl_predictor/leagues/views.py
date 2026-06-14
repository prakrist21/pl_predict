from django.shortcuts import render, redirect
from .forms import LeagueForm, JoinLeagueForm
from .models import League, LeagueMember
from predictions.models import Gameweek, Match, Prediction
from predictions.forms import PredictionForm
from django.db.models import Sum
import uuid
# Create your views here. 843FF1CD

def create_league_view(request):
    if request.method=="POST":
        form=LeagueForm(request.POST)
        if form.is_valid():
            league=form.save(commit=False)
            league.host=request.user
            league.invite_code=uuid.uuid4().hex[:8].upper()
            league.save()
            LeagueMember.objects.create(league=league,user=request.user)
            return redirect('my_leagues')
    else:
        form=LeagueForm()

    return render(request,"leagues/create_league.html",{"form":form})

def join_league_view(request):
    if request.method=='POST':
        form=JoinLeagueForm(request.POST)
        if form.is_valid():
            try: 
                league=League.objects.get(invite_code=form.cleaned_data["invite_code"])
                if league.members.count() >= league.max_players:
                    form.add_error("invite_code","league is full")
                else:
                    LeagueMember.objects.create(league=league,user=request.user)
                    return redirect("my_leagues")
            except League.DoesNotExist:
                form.add_error("invite_code","invalid invite code")
    else:
        form=JoinLeagueForm()
    
    return render(request,'leagues/join_league.html',{"form":form})




def my_leagues_view(request):
    leagues=League.objects.filter(members__user=request.user)
    return render(request,'leagues/my_leagues.html',{"leagues":leagues})

def gw_leaderboard(request,league_id,gw_number):
    league=League.objects.get(id=league_id)
    gameweek=Gameweek.objects.get(number=gw_number)
    members=LeagueMember.objects.filter(league=league)


    users = members.values_list('user', flat=True)
    
    if not LeagueMember.objects.filter(league=league, user=request.user).exists():
        return redirect('my_leagues')
    leaderboard = Prediction.objects.filter(
        user__in=users,
        match__gameweek=gameweek
    ).values('user__username').annotate(
        total_points=Sum('points')
    ).order_by('-total_points')
    
    return render(request, 'leagues/gw_leaderboard.html', {
        'leaderboard': leaderboard,
        'league': league,
        'gameweek': gameweek
    })

def season_leaderboard(request, league_id):
    
    league=League.objects.get(id=league_id)
    members=LeagueMember.objects.filter(league=league)

    users=members.values_list('user',flat=True)
    if not LeagueMember.objects.filter(league=league, user=request.user).exists():
        return redirect('my_leagues')
    leaderboard=Prediction.objects.filter(
        user__in=users,
    ).values('user__username').annotate(total_points=Sum('points')).order_by('-total_points')

    return render(request, 'leagues/season_leaderboard.html', {
        'leaderboard': leaderboard,
        'league': league
    })


def league_gameweeks(request, league_id):
    league = League.objects.get(id=league_id)
    if not LeagueMember.objects.filter(league=league, user=request.user).exists():
        return redirect('my_leagues')
    gameweeks = Gameweek.objects.all()
    return render(request, "predictions/gameweek_list.html", {"gameweek": gameweeks, "league": league})


def league_gameweek_detail(request, league_id, gw_number):
    league = League.objects.get(id=league_id)
    if not LeagueMember.objects.filter(league=league, user=request.user).exists():
        return redirect('my_leagues')
    gameweek = Gameweek.objects.get(number=gw_number)
    matches = Match.objects.filter(gameweek=gameweek)
    return render(request, "predictions/gameweek_detail.html", {
        "matches": matches, "gameweek": gameweek, "league": league
    })


def league_submit_prediction(request, league_id, match_id):
    league = League.objects.get(id=league_id)
    if not LeagueMember.objects.filter(league=league, user=request.user).exists():
        return redirect('my_leagues')
    match = Match.objects.get(match_id=match_id)
    prediction = Prediction.objects.filter(user=request.user, match=match).first()

    if request.method == "POST":
        form = PredictionForm(request.POST)
        if form.is_valid():
            pred_home = form.cleaned_data["pred_home"]
            pred_away = form.cleaned_data["pred_away"]
            if prediction:
                prediction.pred_home = pred_home
                prediction.pred_away = pred_away
                prediction.save()
            else:
                Prediction.objects.create(
                    user=request.user, match=match,
                    pred_away=pred_away, pred_home=pred_home
                )
            return redirect("league_gameweek_detail", league_id=league_id, gw_number=match.gameweek.number)
    else:
        if prediction:
            form = PredictionForm(initial={
                'pred_home': prediction.pred_home,
                'pred_away': prediction.pred_away
            })
        else:
            form = PredictionForm()

    return render(request, "predictions/submit_prediction.html", {
        "form": form, "match": match, "league": league
    })