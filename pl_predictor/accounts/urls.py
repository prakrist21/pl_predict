from django.urls import path
from .views import RegisterView, verify_email, verification_sent
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("register/", RegisterView, name="register"),
    path("verify/<uidb64>/<token>/", verify_email, name="verify_email"),
    path("verification-sent/", verification_sent, name="verification_sent"),
]