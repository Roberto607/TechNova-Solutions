from django.shortcuts import redirect,render
from django.contrib.auth.decorators import login_required, user_passes_test
from products.models import Product, Offer
from django.contrib.auth import get_user_model
from orders.models import Order
 # Obtener estadísticas
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

def is_admin(user):
    return user.is_superuser or user.is_staff

@login_required
@user_passes_test(is_admin, login_url='/usuarios/login/')
def dashboard(request):
 
    
    # Total productos
    total_products = Product.objects.count()
    
    # Total ofertas activas
    total_offers = Offer.objects.filter(is_active=True).count()
    
    # Total usuarios
    total_users = User.objects.count()
    
    # Pedidos de hoy
    today = timezone.now().date()
    today_orders = Order.objects.filter(created_at__date=today).count()
    
    # Pedidos recientes
    recent_orders = Order.objects.order_by('-created_at')[:5]
    
    # Productos más vendidos
    top_products = Product.objects.annotate(
        total_sold=Count('orderitem')
    ).order_by('-total_sold')[:5]
    
    # Usuarios recientes
    recent_users = User.objects.order_by('-date_joined')[:5]
    
    context = {
        'title': 'Panel de Administración',
        'total_products': total_products,
        'total_offers': total_offers,
        'total_users': total_users,
        'today_orders': today_orders,
        'recent_orders': recent_orders,
        'top_products': top_products,
        'recent_users': recent_users,
    }
    return render(request, 'admin_dashboard.html', context)


def is_admin(user):
    return user.is_superuser or user.is_staff

@login_required
@user_passes_test(is_admin, login_url='/usuarios/login/')
def products(request):
    products = Product.objects.all().order_by('-created_at')
    context = {
        'products': products,
        'title': 'Gestionar Productos',
    }
    return render(request, 'admin_products.html', context)

@login_required
@user_passes_test(is_admin, login_url='/usuarios/login/')
def offers(request):
    offers = Offer.objects.all().order_by('-created_at')
    context = {
        'offers': offers,
        'title': 'Gestionar Ofertas',
    }
    return render(request, 'admin_offers.html', context)

@login_required
@user_passes_test(is_admin, login_url='/usuarios/login/')
def users(request):
    users = User.objects.all().order_by('-date_joined')
    context = {
        'users': users,
        'title': 'Gestionar Usuarios',
    }
    return render(request, 'admin_users.html', context)

@login_required
@user_passes_test(is_admin, login_url='/usuarios/login/')
def orders(request):
    orders = Order.objects.all().order_by('-created_at')
    context = {
        'orders': orders,
        'title': 'Gestionar Pedidos',
    }
    return render(request, 'admin_orders.html', context)



