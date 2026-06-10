from django.urls import path
from .views import gameweek_detail, gameweek_list, submit_prediction


urlpatterns = [
    path("gameweeks/",gameweek_list,name="gameweek_list"),
    path("gameweeks/<int:gw_number>/",gameweek_detail,name="gameweek_detail"),
    path('match/<int:match_id>/predict/', submit_prediction, name='submit_prediction'),


]
