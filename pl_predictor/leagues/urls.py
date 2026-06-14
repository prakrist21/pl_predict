from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_league_view, name='create_league'),
    path('join/', views.join_league_view, name='join_league'),
    path('my/', views.my_leagues_view, name='my_leagues'),
    path('<int:league_id>/gw/<int:gw_number>/', views.gw_leaderboard, name='gw_leaderboard'),
    path('<int:league_id>/season/', views.season_leaderboard, name='season_leaderboard'),
    path('<int:league_id>/gameweeks/', views.league_gameweeks, name='league_gameweeks'),
    path('<int:league_id>/gameweeks/<int:gw_number>/', views.league_gameweek_detail, name='league_gameweek_detail'),
    path('<int:league_id>/match/<int:match_id>/predict/', views.league_submit_prediction, name='league_submit_prediction'),
]