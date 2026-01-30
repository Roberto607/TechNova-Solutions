from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.dashboard, name='admin_dashboard'),
    path('productos/', views.products, name='admin_products'),
    path('productos/add/', views.product_add, name='admin_product_add'),
    path('productos/<int:pk>/', views.product_detail, name='admin_product_detail'),
    path('productos/<int:pk>/edit/', views.product_edit, name='admin_product_edit'),
    path('productos/<int:pk>/delete/', views.product_delete, name='admin_product_delete'),
    path('ofertas/', views.offers, name='admin_offers'),
    path('ofertas/add/', views.offer_add, name='admin_offer_add'),
    path('ofertas/<int:pk>/', views.offer_detail, name='admin_offer_detail'),
    path('ofertas/<int:pk>/edit/', views.offer_edit, name='admin_offer_edit'),
    path('ofertas/<int:pk>/delete/', views.offer_delete, name='admin_offer_delete'),
    path('usuarios/', views.users, name='admin_users'),
    path('usuarios/<int:pk>/', views.user_detail, name='admin_user_detail'),
    path('usuarios/<int:pk>/edit/', views.user_edit, name='admin_user_edit'),
    path('usuarios/<int:pk>/permissions/', views.user_permissions, name='admin_user_permissions'),
    path('pedidos/', views.orders, name='admin_orders'),
    path('pedidos/<int:pk>/', views.order_detail, name='admin_order_detail'),
    path('pedidos/<int:pk>/update/', views.order_update_status, name='admin_order_update'),
]
