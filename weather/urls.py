from django.urls import path
from .views import weather_view

urlpatterns = [
    path('name/', weather_view, name='name'),
    path('coord/', weather_view, name='coord')
]