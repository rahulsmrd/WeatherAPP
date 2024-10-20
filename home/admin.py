from django.contrib import admin
from home.models import WeatherModel, DailyWeatherModel, alerts, City

# Register your models here.
admin.site.register(WeatherModel)
admin.site.register(DailyWeatherModel)
admin.site.register(alerts)
admin.site.register(City)