from urllib.parse import urlparse

from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
import requests

from .forms import SiteForm
from .models import Site, SiteStatistics


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


def update_site_statistics(site, request, response):
    statistics, _ = SiteStatistics.objects.get_or_create(site=site)

    request_header_size = len(str(request.META).encode('utf-8'))
    request_body_size = (len(response.request.body) if response.request.body else 0)
    sent_data_size = request_header_size + request_body_size

    response_header_size = len(str(response.headers).encode('utf-8'))
    response_body_size = len(response.content)
    received_data_size = response_header_size + response_body_size

    statistics.page_views += 1
    statistics.data_sent += sent_data_size
    statistics.data_received += received_data_size
    statistics.save()


@login_required
def proxy_site(request, user_site_name, routes_on_original_site):
    site = get_object_or_404(Site, user=request.user, name=user_site_name)
    parsed_original_site = urlparse(routes_on_original_site)

    response = requests.get(routes_on_original_site)

    update_site_statistics(site, request, response)

    soup = BeautifulSoup(response.content, "html.parser")
    for link in soup.find_all("a", href=True):
        parsed_href = urlparse(link["href"])
        if (parsed_href.scheme == parsed_original_site.scheme
            and parsed_href.netloc == parsed_original_site.netloc
        ):
            link["href"] = f"/{user_site_name}/{link['href']}"

    return HttpResponse(str(soup))


def convert_bytes_to_another_unit(byte_size):
    size_units = ['B', 'KB', 'MB', 'GB']

    unit_index = 0
    while byte_size >= 1024 and unit_index < len(size_units) - 1:
        byte_size /= 1024.0
        unit_index += 1

    formatted_size = f"{byte_size:.2f} {size_units[unit_index]}"

    return formatted_size


def user_site_statistics(request):
    site_statistics = SiteStatistics.objects.filter(site__user=request.user)

    sites_instances = []
    for site in site_statistics:
        site.data_sent = convert_bytes_to_another_unit(site.data_sent)
        site.data_received = convert_bytes_to_another_unit(site.data_received)
        sites_instances.append(site)

    return render(request, 'sites/user_site_statistics.html', {'site_statistics': site_statistics})
