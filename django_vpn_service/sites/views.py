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


def update_site_data_statistics(site, request, response):
    statistics, _ = SiteStatistics.objects.get_or_create(site=site)

    request_header_size = len(str(request.META).encode("utf-8"))
    request_body_size = (len(response.request.body) if response.request.body else 0)
    sent_data_size = request_header_size + request_body_size

    response_header_size = len(str(response.headers).encode("utf-8"))
    response_body_size = len(response.content)
    received_data_size = response_header_size + response_body_size

    statistics.data_sent += sent_data_size
    statistics.data_received += received_data_size
    statistics.save()


def update_site_counter(site):
    statistics, _ = SiteStatistics.objects.get_or_create(site=site)
    statistics.page_views += 1
    statistics.save()


# Endpoint for main site page
@login_required
def proxy_site(request, user_site_name, site_url):
    site = get_object_or_404(Site, user=request.user, name=user_site_name)
    parsed_original_site = urlparse(site_url)

    response = requests.get(site_url)

    update_site_data_statistics(site, request, response)
    update_site_counter(site)

    # Proxy site links
    soup = BeautifulSoup(response.content, "html.parser")
    for link in soup.find_all("a", href=True):
        parsed_href = urlparse(link["href"])
        if (parsed_href.scheme == parsed_original_site.scheme
            and parsed_href.netloc == parsed_original_site.netloc
        ):
            link["href"] = f"/{user_site_name}/{link['href']}"
        if not parsed_href.scheme and not parsed_href.netloc:
            link[
                "href"] = (f"/{user_site_name}/{parsed_original_site.scheme}://{parsed_original_site.netloc}"
                           f"{link['href']}")

    # Proxy additional data links
    for tag in soup.find_all(["link"], href=True):
        parsed_data_href = urlparse(tag["href"])
        if (parsed_data_href.scheme == parsed_original_site.scheme
            and parsed_data_href.netloc == parsed_original_site.netloc
        ):
            tag["href"] = f'/data/{user_site_name}/{tag["href"]}'
        if not parsed_data_href.scheme and not parsed_data_href.netloc:
            tag[
                "href"] = (f"/data/{user_site_name}/{parsed_original_site.scheme}://{parsed_original_site.netloc}"
                           f"{tag['href']}")

    for tag in soup.find_all(["img","script", "audio", "video", "source"], src=True):
        parsed_src_href = urlparse(tag["src"])
        if (parsed_src_href.scheme == parsed_original_site.scheme
            and parsed_src_href.netloc == parsed_original_site.netloc
        ):
            tag["src"] = f'/data/{user_site_name}/{tag["src"]}'
        if not parsed_src_href.scheme and not parsed_src_href.netloc:
            tag[
                "src"] = (f"/data/{user_site_name}/{parsed_original_site.scheme}://{parsed_original_site.netloc}"
                          f"{tag['src']}")

    return HttpResponse(str(soup))


# Endpoint for additional page data
def proxy_data(request, user_site_name, data_url):
    site = get_object_or_404(Site, user=request.user, name=user_site_name)
    response = requests.get(data_url)

    update_site_data_statistics(site, request, response)

    django_response = HttpResponse(content=response.content, status=response.status_code)
    for header, value in response.headers.items():
        if header in (
            "Connection",
            "Keep-Alive",
            "Proxy-Authenticate",
            "Proxy-Authorization",
            "TE",
            "Trailers",
            "Transfer-Encoding",
            "Upgrade"
        ):
            continue
        django_response[header] = value

    return django_response


def convert_bytes_to_another_unit(byte_size):
    size_units = ["B", "KB", "MB", "GB"]

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

    return render(request, "sites/user_site_statistics.html", {"site_statistics": site_statistics})
