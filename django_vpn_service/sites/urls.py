from django.urls import path

from .views import create_site

urlpatterns = [
    path('create_site/', create_site, name='create_site')
]
