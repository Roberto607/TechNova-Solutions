from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.dashboard, name='admin_dashboard'),
    path('productos/', views.products, name='admin_products'),
    path('ofertas/', views.offers, name='admin_offers'),
    path('usuarios/', views.users, name='admin_users'),
    path('pedidos/', views.orders, name='admin_orders'),
]
