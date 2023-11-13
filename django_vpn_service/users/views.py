from django.contrib.auth import login as auth_login
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, RegistrationForm


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("home")
        else:
            print("Form is invalid", flush=True)
            print(form.errors)
    else:
        form = RegistrationForm()
    return render(request, "users/register.html", {"form": form})


def login(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


@login_required
def home(request):
    return render(request, "users/home.html", {"user": request.user})
