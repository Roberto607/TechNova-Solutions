"""
URLs de la aplicación orders
Configuración de rutas para gestión de pedidos y carritos
"""

from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # URLs para carrito
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<slug:product_slug>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    
    
    # URLs para checkout
    path('contacto/', views.contact_info, name='contact_info'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/confirm/', views.checkout_confirm, name='checkout_confirm'),
    path('checkout/success/<str:order_number>/', views.order_success, name='order_success'),
    
    # URLs para pedidos
    path('orders/', views.order_list, name='orders'),
    path('orders/<str:order_number>/', views.order_detail, name='order_detail'),
    path('orders/<str:order_number>/cancel/', views.cancel_order, name='cancel_order'),
    
    # URLs para wishlist
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<slug:product_slug>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
]