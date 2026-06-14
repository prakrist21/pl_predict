from django.shortcuts import render, redirect
from .forms import LeagueForm, JoinLeagueForm
from .models import League, LeagueMember

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