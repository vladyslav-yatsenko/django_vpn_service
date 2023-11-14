from django.urls import path

from .views import login, logout, register, user_profile

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("profile/", user_profile, name="user_profile"),
]
