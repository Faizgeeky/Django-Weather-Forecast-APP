
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.check_weather, name='check_weather'),
    path('forecast/', views.forecast , name='weatherforecast')

   
]