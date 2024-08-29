from django.db import models
from django.db.models import Model

# Create your models here.

class CityWeather(models.Model):
    # id  = models.IntegerField(primary_key=True)
    city = models.CharField(max_length=250)
    temp_c = models.FloatField(null=False)
    temp_f = models.FloatField(null=False)
    date = models.DateTimeField()
    