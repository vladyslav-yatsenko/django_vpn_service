from django.urls import path

from .views import create_site, home, proxy_site, user_site_statistics, proxy_data

urlpatterns = [
    path("create_site/", create_site, name="create_site"),
    path("home/", home, name="home"),
    path("data/<str:user_site_name>/<path:data_url>/", proxy_data, name="proxy_data"),
    path("<str:user_site_name>/<path:site_url>/", proxy_site, name="proxy_site"),
    path("user_site_statistics/", user_site_statistics, name="user_site_statistics"),
]
