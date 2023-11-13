from django.urls import path

from .views import home, login, register

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("home/", home, name="home")
]
