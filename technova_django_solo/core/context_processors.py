"""
Context processors para TechNova Solutions
Proporcionan datos globales a todas las plantillas
"""

from orders.models import Cart, CartItem
from products.models import Category


def cart(request):
    """Contexto del carrito de compras"""
    cart_items = []
    cart_total = 0
    cart_count = 0
    
    if request.user.is_authenticated:
        # Usuario autenticado
        cart_obj, created = Cart.objects.get_or_create(user=request.user)
    else:
        # Usuario anónimo
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        
        cart_obj, created = Cart.objects.get_or_create(session_id=session_key)
    
    cart_items = cart_obj.items.select_related('product').all()
    cart_count = sum(item.quantity for item in cart_items)
    cart_total = sum(item.total_price for item in cart_items)
    
    return {
        'cart': cart_obj,
        'cart_items': cart_items,
        'cart_count': cart_count,
        'cart_total': cart_total,
    }


def categories(request):
    """Contexto de categorías"""
    categories = Category.objects.filter(
        parent__isnull=True,
        is_active=True
    ).order_by('sort_order')
    
    return {
        'main_categories': categories,
    }