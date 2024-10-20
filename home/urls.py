from django.urls import path
from home.views import home, add_city, create_alerts, myAlerts, update_weather, chartVisualization, delete_city

app_name = 'home'

urlpatterns = [
    path('', home, name='home'),
    path('update/', update_weather, name='update'),
    path('add_city/', add_city, name='add_city'),
    path('create_alert/', create_alerts, name='create_alert'),
    path('my_alerts/', myAlerts, name='my_alerts'),
    path('visualize/<str:city>/', chartVisualization, name='visualize'),
    path('delete/<str:city>/', delete_city, name='delete'),
]