from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.home, name='home'),
    path('categoria/<slug:category_slug>/', views.category_view, name='category'),
    path('producto/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='detail'),
    path('buscar/', views.search, name='search'),
    path('todos/', views.all_products, name='all'),  # Nueva URL para ver todos los productos
    path('ofertas/', views.sale_products, name='sale'),  # Nueva URL para productos en oferta
    path('ofertas/<int:offer_id>/', views.offer_detail, name='offer_detail'),
]
