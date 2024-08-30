from django.db import models
from django.db.models import Model


class CityWeather(models.Model):
    id  = models.AutoField(primary_key=True)
    city = models.CharField(max_length=250)
    temp_c = models.FloatField(null=False)
    temp_f = models.FloatField(null=False)
    humidity = models.FloatField(null=False)
    date = models.DateTimeField()
    country = models.CharField(max_length=250)