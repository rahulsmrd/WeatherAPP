from django.shortcuts import render, redirect
from django.urls import reverse
import datetime
from home.models import WeatherModel, City, DailyWeatherModel, alerts
from jobs.jobs import fetch_weather, check_alerts, get_cities_and_update_DB

# Create your views here.
def home(request):
    weather = []
    alerts_list = []
    cities = City.objects.all()
    for city in cities:
        weather_data = WeatherModel.objects.filter(city=city).last()
        weather_data.timestamp = datetime.datetime.now()
        weather_data.save()
        weather.append(weather_data)
        alert, val = check_alerts(city, weather_data)
        if alert:
            alerts_list.extend(val)
    return render(request, 'home.html', {'weather': weather, 'alerts': alerts_list})

def add_city(request):
    if request.method == 'POST':
        city_name = request.POST['city_name']
        country = request.POST['country']
        city_obj = City.objects.create(name=city_name, country=country)
        try:
            fetch_weather(city_name=city_name)
        except Exception as e:
            city_obj.delete()
            return render(request, 'add_city.html', {'error': f'Error fetching weather for {city_name}, please try again'})
        return redirect(reverse('home:home'))
    return render(request, 'add_city.html')

def create_alerts(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        city_obj = City.objects.get(name=city)
        alerts.objects.create(
            city=city_obj,
            alert_type=request.POST.get('alert_on'),
            alert_condition=request.POST.get('alert_condition'),
            alert_value=request.POST.get('alert_val'),
        )
        return redirect(reverse('home:home'))
    return render(request, 'create_alerts.html', {'cities': City.objects.all()})

def myAlerts(request):
    alerts_q = alerts.objects.all()
    return render(request, 'my_alerts.html', {'alerts': alerts_q})

def chartVisualization(request, city):
    days = DailyWeatherModel.objects.filter(city__name=city).all()
    if not days:
         return render(request, 'daily_aggregates.html', {'cities': City.objects.all(), 'error': f'No data available for this city ({city}).'})
    min_temperature = [['Date','Temperature']]
    max_temperature = [['Date','Temperature']]
    avg_temperature = [['Date','Temperature']]
    max_humidity = [['Date','Humidity']]
    max_wind_speed = [['Date','Speed']]
    weather_condition = [['Date','Condition']]
    types = {}
    types_list = []
    for day in days:
        min_temperature.append([str(day.date),day.min_temperature])
        max_temperature.append([str(day.date),day.max_temperature])
        avg_temperature.append([str(day.date),day.avg_temperature])
        max_humidity.append([str(day.date),day.max_humidity])
        max_wind_speed.append([str(day.date),day.max_wind_speed])
        if day.weather_condition not in types:
            types[day.weather_condition] = len(types) + 1
            types_list.append([day.weather_condition, types[day.weather_condition]])
        weather_condition.append([str(day.date),types[day.weather_condition]])
    return render(
            request,
            'daily_aggregates.html',
            {
                'city': city,
                'min_temperature': min_temperature,
                'max_temperature': max_temperature,
                'avg_temperature': avg_temperature,
                'weather_condition': weather_condition,
                'max_humidity': max_humidity,
                'max_wind_speed': max_wind_speed,
                'types': types_list,
                'cities': City.objects.all()
            }
        )

def delete_city(request, city):
    city_obj = City.objects.get(name=city)
    city_obj.delete()
    return redirect(reverse('home:home'))