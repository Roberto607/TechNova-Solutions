

# Vista de ejemplo para el perfil de usuario
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Category, Product, ProductImage, Review

def home(request):
    """Vista principal con productos destacados y categorías"""
    featured_products = Product.objects.filter(
        status='active',
        stock_quantity__gt=0
    ).select_related('category').prefetch_related('additional_images')[:8]
    
    categories = Category.objects.filter(
        is_active=True,
        parent=None
    ).order_by('sort_order')
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'templates/products/home.html', context)

def category_view(request, category_slug):
    """Vista de categoría con productos y subcategorías"""
    category = get_object_or_404(Category, slug=category_slug)
    
    # Obtener productos de esta categoría y subcategorías
    products = Product.objects.filter(
        Q(category=category) | Q(category__parent=category),
        status='active',
        stock_quantity__gt=0
    ).select_related('category').prefetch_related('additional_images')
    
    # Obtener subcategorías
    subcategories = category.children.filter(is_active=True)
    
    context = {
        'category': category,
        'products': products,
        'subcategories': subcategories,
    }
    return render(request, 'category.html', context)

def product_detail(request, category_slug, product_slug):
    """Vista de detalle de producto con imágenes y reseñas"""
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(
        Product.objects.select_related('category')
        .prefetch_related('additional_images', 'reviews__user'),
        slug=product_slug,
        category=category
    )
    
    # Obtener productos relacionados
    related_products = Product.objects.filter(
        category=category,
        status='active',
        stock_quantity__gt=0
    ).exclude(id=product.id)[:4]
    
    # Obtener reseñas aprobadas
    approved_reviews = product.reviews.filter(is_approved=True)
    
    context = {
        'product': product,
        'category': category,
        'related_products': related_products,
        'approved_reviews': approved_reviews,
    }
    return render(request, 'detail.html', context)

def search(request):
    """Vista de búsqueda de productos"""
    query = request.GET.get('q', '')
    products = Product.objects.none()
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__icontains=query) |
            Q(category__name__icontains=query),
            status='active',
            stock_quantity__gt=0
        ).select_related('category').prefetch_related('additional_images')
    
    context = {
        'query': query,
        'products': products,
    }
    return render(request, 'search.html', context)


def all_products(request):
    """Vista para mostrar todos los productos activos"""
    products = Product.objects.filter(
        status='active',
        stock_quantity__gt=0
    ).select_related('category').prefetch_related('additional_images')
    
    context = {
        'products': products,
        'title': 'Todos los Productos',
    }
    return render(request, 'all.html', context)

def sale_products(request):
    """Vista para mostrar productos en oferta"""
    products = Product.objects.filter(
        status='active',
        stock_quantity__gt=0,
        compare_at_price__isnull=False
    ).select_related('category').prefetch_related('additional_images')
    
    context = {
        'products': products,
        'title': 'Productos en Oferta',
    }
    return render(request, 'sale.html', context)


