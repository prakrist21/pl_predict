from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_league_view, name='create_league'),
    path('join/', views.join_league_view, name='join_league'),
    path('my/', views.my_leagues_view, name='my_leagues'),
]