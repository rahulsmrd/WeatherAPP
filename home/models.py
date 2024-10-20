from django.db import models

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

class WeatherModel(models.Model):
    city = models.ForeignKey('City', null=True, blank=True, on_delete=models.CASCADE, related_name='weather')
    temperature = models.FloatField()
    weather_condition = models.CharField(max_length=50)
    feels_like = models.FloatField()
    humidity = models.FloatField(default=0.00)
    wind_speed = models.FloatField(default=0.00)
    timestamp = models.DateTimeField(auto_now=True)

class DailyWeatherModel(models.Model):
    city = models.ForeignKey('City', null=True, blank=True, on_delete=models.CASCADE, related_name='daily_weather')
    date = models.DateField()
    avg_temperature = models.FloatField()
    min_temperature = models.FloatField()
    max_temperature = models.FloatField()
    max_wind_speed = models.FloatField(default=0.00)
    max_humidity = models.FloatField(default=0.00)
    weather_condition = models.CharField(max_length=50)

class alerts(models.Model):
    city = models.ForeignKey('City', null=True, blank=True, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=50)
    alert_condition = models.CharField(max_length=20)
    alert_value = models.CharField(max_length=200)