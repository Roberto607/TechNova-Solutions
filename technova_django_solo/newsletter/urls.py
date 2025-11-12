from django.urls import path
from . import views

app_name = 'newsletter'

urlpatterns = [
    path('suscribir/', views.subscribe, name='subscribe'),
]
