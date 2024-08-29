from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .models import CityWeather
import requests

api_key = settings.WEATHER_API
url = 'http://api.weatherapi.com/v1'

def home(request):
    return HttpResponse("Hello world!")


def get_weather(cities):
    city_weather_list = []
    if len(cities) >0:
        for city in cities:
            url_weather = f'{url}/current.json?key={api_key}&q={city}'
            response = requests.get(url_weather)
            if response.status_code == 200:
                data = response.json()
                temp_city = {}
                temp_city['city'] = data['location']['name']
                temp_city['temp_c'] = str(data['current']['temp_c'])
                temp_city['temp_f'] = data['current']['temp_f']
                temp_city['date'] = data['location']['localtime']
                city_weather_list.append(temp_city)
        return city_weather_list
    else:
        return None

def check_weather(request):
    cities = ['maxico','london']
    weather_data = get_weather(cities)
    print("Data us", weather_data)
    try:
        city_weather_instances = [
            CityWeather(
                city=data['city'],
                temp_c=data['temp_c'],
                temp_f=data['temp_f'],
                date=data['date']
            ) for data in weather_data
        ]
        
        CityWeather.objects.bulk_create(city_weather_instances)
    except Exception as e:
        return render(request, "index.html", {
            "error": f"Something went wrong adding data: {str(e)}",
            "data": weather_data
        })

    return render(request, 'index.html', {"data": weather_data})