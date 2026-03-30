from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('index/', views.index, name='index'),
    path('smart/',views.smart,name='smart'),
    path('model-prediction/', views.model_prediction, name='model-prediction'),
    path('search/', views.search, name='search'),
    path('user/index/<str:page>.html', views.dynamic_user_page, name='dynamic_user_page'),
]