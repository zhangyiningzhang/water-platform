from django.urls import path
from .views import get_sensor_data

urlpatterns = [
    path('sensor-data/', get_sensor_data, name='get_sensor_data'),
]