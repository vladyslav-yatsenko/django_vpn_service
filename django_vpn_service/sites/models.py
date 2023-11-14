from django.db import models

from users.models import User


class Site(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    url = models.URLField()

    def __str__(self):
        return self.name


class SiteStatistics(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    page_views = models.IntegerField(default=0)
    data_sent = models.IntegerField(default=0)
    data_received = models.IntegerField(default=0)

    def __str__(self):
        return self.site.name
