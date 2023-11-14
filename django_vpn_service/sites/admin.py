from django.contrib import admin

from .models import Site, SiteStatistics

admin.site.register(Site)
admin.site.register(SiteStatistics)
