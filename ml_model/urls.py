# your_project/ml_model/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict_random, name='predict_random'),
]