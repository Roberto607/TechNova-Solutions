"""
Vistas principales de TechNova Solutions
Páginas principales del sitio web
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from products.models import Product, Category
from orders.models import Cart, CartItem
from core.models import ContactMessage
from .forms import ContactForm


def home(request):
    """Página principal del sitio"""
    # Productos destacados
    featured_products = Product.objects.filter(
        status='active'
    ).order_by('-created_at')[:8]
    
    # Productos en oferta
    sale_products = Product.objects.filter(
        status='active',
        compare_at_price__isnull=False
    ).order_by('-created_at')[:6]
    
    # Productos mejor valorados
    top_rated_products = Product.objects.filter(
        status='active',
        average_rating__gte=4.0
    ).order_by('-average_rating')[:6]
    
    # Categorías principales
    main_categories = Category.objects.filter(
        parent__isnull=True,
        is_active=True
    ).order_by('sort_order')[:6]
    
    context = {
        'featured_products': featured_products,
        'sale_products': sale_products,
        'top_rated_products': top_rated_products,
        'main_categories': main_categories,
    }
    
    return render(request, 'home.html', context)


def about(request):
    """Página acerca de nosotros"""
    return render(request, 'core/about.html')


def contact(request):
    """Página de contacto"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu mensaje ha sido enviado correctamente. Te contactaremos pronto.')
            return redirect('core:contact')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def terms(request):
    """Términos y condiciones"""
    return render(request, 'core/terms.html')


def privacy(request):
    """Política de privacidad"""
    return render(request, 'core/privacy.html')


def search(request):
    """Búsqueda de productos"""
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort', '-created_at')
    
    products = Product.objects.filter(status='active')
    
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__icontains=query) |
            Q(sku__icontains=query)
        )
    
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    if min_price:
        products = products.filter(price__gte=min_price)
    
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Ordenamiento
    if sort_by in ['price', '-price', 'name', '-name', 'average_rating', '-average_rating']:
        products = products.order_by(sort_by)
    else:
        products = products.order_by('-created_at')
    
    # Paginación
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'products': page_obj,
        'query': query,
        'category_slug': category_slug,
        'sort_by': sort_by,
        'page_obj': page_obj,
    }
    
    return render(request, 'core/search.html', context)


def error_400(request, exception):
    """Manejo de error 400"""
    return render(request, 'core/errors/400.html', status=400)


def error_403(request, exception):
    """Manejo de error 403"""
    return render(request, 'core/errors/403.html', status=403)


def error_404(request, exception):
    """Manejo de error 404"""
    return render(request, 'core/errors/404.html', status=404)


def error_500(request):
    """Manejo de error 500"""
    return render(request, 'core/errors/500.html', status=500)