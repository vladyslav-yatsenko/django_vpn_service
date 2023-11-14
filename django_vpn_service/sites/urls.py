from django.urls import path

from .views import create_site, home, proxy_site, user_site_statistics

urlpatterns = [
    path("create_site/", create_site, name="create_site"),
    path("home/", home, name="home"),
    path("<str:user_site_name>/<path:routes_on_original_site>/", proxy_site, name="proxy_site"),
    path('user_site_statistics/', user_site_statistics, name='user_site_statistics'),
]
