import requests
from home.models import WeatherModel, City, DailyWeatherModel, alerts
from django.db.models import Avg, Max, Min
import datetime

def fetch_weather(city_name):
    api_key = 'ae69cc3b9b0cb63bb54c14e4cfad88c3'
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
    try:
        response = requests.get(url)
    except Exception as e:
        return e
    data = response.json()
    # Extract relevant weather information
    temp_kelvin = data['main']['temp']
    temp_celsius = temp_kelvin - 273.15  # Convert to Celsius
    feels_like_celsius = data['main']['feels_like'] - 273.15
    weather_condition = data['weather'][0]['main']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    city, create = City.objects.get_or_create(
        name = city_name,
        country = data['sys']['country'],
    )
    weather_data = WeatherModel.objects.create(
        city = city,
        temperature = temp_celsius,
        weather_condition = weather_condition,
        feels_like = feels_like_celsius,
        humidity = humidity,
        wind_speed = wind_speed,
    )
    return check_alerts(city, weather_data)


def get_cities_and_update_DB():
    print('Database Populating ...')
    cities = City.objects.values_list('name', flat=True).all()
    for city in cities:
        fetch_weather(city)


def get_aggregates():
    print('Getting aggregates ...')
    cities = City.objects.all()
    for city in cities:
        weather_data = WeatherModel.objects.filter(city=city).filter(timestamp__date = datetime.datetime.now().date())
        weather_conditions = list(weather_data.values_list('weather_condition', flat=True))
        city_data = {
            'city': city,
            'avg_temperature': weather_data.aggregate(Avg('temperature'))['temperature__avg'],
            'max_temperature': weather_data.aggregate(Max('temperature'))['temperature__max'],
            'min_temperature': weather_data.aggregate(Min('temperature'))['temperature__min'],
            'max_humidity': weather_data.aggregate(Max('humidity'))['humidity__max'],
            'max_wind_speed': weather_data.aggregate(Max('wind_speed'))['wind_speed__max'],
            'weather_condition': max(set(weather_conditions), key=weather_conditions.count),
            'date' : datetime.date.today(),
        }
        DailyWeatherModel.objects.create(**city_data)


def check_alerts(city, weather_data):
    city_alerts = alerts.objects.filter(city = city).all()
    if not city_alerts:
        return False, None
    alerts_list = []
    for alert in city_alerts:
        if alert.alert_condition == '>':
            x = getattr(weather_data, alert.alert_type)
            if str(x) > alert.alert_value:
                alerts_list.append(f"Alert: {alert.alert_type} {alert.alert_condition} {alert.alert_value} in {city.name}")
                print(f"Alert: {alert.alert_type} {alert.alert_condition} {alert.alert_value} in {city.name}")
        elif alert.alert_condition == '<':
            x = getattr(weather_data, alert.alert_type)
            if str(x) < alert.alert_value:
                alerts_list.append(f"Alert: {alert.alert_type} {alert.alert_condition} {alert.alert_value} in {city.name}")
                print(f"Alert: {alert.alert_type} {alert.alert_condition} {alert.alert_value} in {city.name}")
        else:
            x = getattr(weather_data, alert.alert_type)
            if str(x) == alert.alert_value:
                alerts_list.append(f"Alert: {alert.alert_type} {alert.alert_condition} {alert.alert_value} in {city.name}")
                print(f"Alert: {alert.alert_type} {alert.alert_condition} {alert.alert_value} in {city.name}")
    if len(alerts_list) > 0:
        return True, alerts_list
    return False, []