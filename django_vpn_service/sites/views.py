from urllib.parse import urlparse

from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
import requests

from .forms import SiteForm
from .models import Site


@login_required
def create_site(request):
    if request.method == "POST":
        form = SiteForm(request.POST)
        if form.is_valid():
            site = form.save(commit=False)
            site.user = request.user
            site.save()
            return redirect("home")
        else:
            print(f"Form is invalid {form.errors = }")
    else:
        form = SiteForm()
    return render(request, "sites/create_site.html", {"form": form})


@login_required
def home(request):
    user_sites = Site.objects.filter(user=request.user)
    return render(request, "sites/home.html", {"user_sites": user_sites, "user": request.user})


def proxy_site(request, user_site_name, routes_on_original_site):
    get_object_or_404(Site, user=request.user, name=user_site_name)
    parsed_original_site = urlparse(routes_on_original_site)

    response = requests.get(routes_on_original_site)
    content = response.content

    soup = BeautifulSoup(content, "html.parser")
    for link in soup.find_all("a", href=True):
        parsed_href = urlparse(link["href"])
        if (parsed_href.scheme == parsed_original_site.scheme
            and parsed_href.netloc == parsed_original_site.netloc
        ):
            link["href"] = f"/{user_site_name}/{link['href']}"

    return HttpResponse(str(soup))
