"""
URLs de la aplicación core
Configuración de rutas para funcionalidades centrales
"""

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # APIs específicas del core si las hay
    path('', views.home, name='home'),
    path('contacto/', views.contact, name='contact'),
]