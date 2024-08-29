from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .models import CityWeather
import requests
import datetime
from django.db.models import Avg, Max, Min


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
                temp_city['temp_c'] = float(data['current']['temp_c'])
                temp_city['temp_f'] = float(data['current']['temp_f'])
                temp_city['date'] = data['location']['localtime']
                city_weather_list.append(temp_city)
        return city_weather_list
    else:
        return None

def check_weather(request):
    if request.method == "GET":
        return render(request,"index.html")
    elif request.method == "POST":
        # get cities need forecast for
        cities = request.POST.get('cities').split(",")
        

        if cities:
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
        else:
            return render(request,'index.html',{"message":"Cities not found in Req body!"} )
        
        return render(request, 'index.html', {"data": weather_data} , )
    


def forecast(request):
    if request.method == "GET":
        return render(request, 'forecast.html')
    elif request.method == "POST":
        cities = request.POST.get('cities').split(",")


        last_24_hrs =  datetime.datetime.now() - datetime.timedelta(days=1)

        print(last_24_hrs)
        if cities:
            city_object = {}
            for city in cities:
                data = CityWeather.objects.filter(city = city ,date__gt=last_24_hrs)
                data = data.aggregate(
                    avg_temp_c = Avg('temp_c'),
                    max_temp_c = Avg('temp_c'),
                    min_temp_c = Avg('temp_c'),

                    avg_temp_f = Avg('temp_f'),
                    max_temp_f = Avg('temp_f'),
                    min_temp_f = Avg('temp_f'),

                )
                
                city_object[city] = data

    print(city_object)        
    return render(request, 'forecast.html', {'data':city_object})