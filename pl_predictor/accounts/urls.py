from django.urls import path
from .views import RegisterView


urlpatterns = [
    path("register/",RegisterView, name="register"),
    # path("login/",),
    # path("logout/",),
]