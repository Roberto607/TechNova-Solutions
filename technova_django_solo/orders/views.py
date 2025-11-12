"""
Vistas para la aplicación orders
Gestión de carritos, pedidos y listas de deseos
"""
import random
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.core.paginator import Paginator
from products.models import Product
from .models import Cart, CartItem, Order, OrderItem, Wishlist


@login_required
def cart_view(request):
    """Ver carrito de compras"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product').all()
    cart_total = sum(item.total_price for item in cart_items)
    cart_count = sum(item.quantity for item in cart_items)
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_count': cart_count,
    }
    
    return render(request, 'cart.html', context)


@login_required
def add_to_cart(request, product_slug):
    """Agregar producto al carrito"""
    product = get_object_or_404(Product, slug=product_slug, status='active')
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity <= 0:
            messages.error(request, 'La cantidad debe ser mayor a 0')
            return redirect('products:product_detail', category_slug=product.category.slug, product_slug=product_slug)
        
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Verificar si el producto ya está en el carrito
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # Si ya existe, sumar la cantidad
            cart_item.quantity += quantity
            cart_item.save()
        
        messages.success(request, f'{product.name} agregado al carrito')
        return redirect('orders:cart')
    
    return redirect('products:detail', category_slug=product.category.slug, product_slug=product_slug)


@login_required
def remove_from_cart(request, item_id):
    """Remover item del carrito"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    
    messages.success(request, f'{product_name} removido del carrito')
    return redirect('orders:cart')


@login_required
def update_cart(request):
    """Actualizar cantidades del carrito"""
    if request.method == 'POST':
        cart = Cart.objects.get(user=request.user)
        
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                item_id = key.split('_')[1]
                try:
                    quantity = int(value)
                    cart_item = CartItem.objects.get(id=item_id, cart=cart)
                    
                    if quantity <= 0:
                        cart_item.delete()
                    else:
                        cart_item.quantity = quantity
                        cart_item.save()
                        
                except (ValueError, CartItem.DoesNotExist):
                    continue
        
        messages.success(request, 'Carrito actualizado')
        return redirect('orders:cart')
    
    return redirect('orders:cart')


@login_required
def checkout(request):
    """Página de checkout"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product').all()
    
    if not cart_items:
        messages.warning(request, 'Tu carrito está vacío')
        return redirect('core:home')
    
    cart_total = sum(item.total_price for item in cart_items)
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    
    return render(request, 'checkout.html', context)


@login_required
def checkout_confirm(request):
    """Confirmar pedido"""
    if request.method != 'POST':
        return redirect('orders:checkout')
    
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.select_related('product').all()
    
    if not cart_items:
        messages.warning(request, 'Tu carrito está vacío')
        return redirect('core:home')
    
    # Generar número de pedido
    order_number = f"ORD{random.randint(100000, 999999)}"
    
    with transaction.atomic():
        # Crear orden
        order = Order.objects.create(
            user=request.user,
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            shipping_address={
                'address': request.POST.get('shipping_address'),
                'city': request.POST.get('shipping_city'),
                'postal_code': request.POST.get('shipping_postal'),
            },
            billing_address={
                'address': request.POST.get('billing_address') if not request.POST.get('same_as_shipping') else request.POST.get('shipping_address'),
                'city': request.POST.get('billing_city') if not request.POST.get('same_as_shipping') else request.POST.get('shipping_city'),
                'postal_code': request.POST.get('billing_postal') if not request.POST.get('same_as_shipping') else request.POST.get('shipping_postal'),
            },
            payment_method=request.POST.get('payment_method'),
            subtotal=sum(item.total_price for item in cart_items),
            total_amount=sum(item.total_price for item in cart_items),
            order_number=order_number,
        )
        
        # Crear items de la orden
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                unit_price=cart_item.product.price,
                total_price=cart_item.total_price,
            )
        
        # Limpiar carrito
        cart.items.all().delete()
    
    messages.success(request, f'Orden {order_number} creada exitosamente')
    return redirect('orders:order_success', order_number=order_number)


@login_required
def order_success(request, order_number):
    """Página de éxito del pedido"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    context = {
        'order': order,
    }
    
    return render(request, 'success.html', context)


@login_required
def order_list(request):
    """Lista de pedidos del usuario"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'orders': page_obj,
        'page_obj': page_obj,
    }
    
    return render(request, 'order_list.html', context)


@login_required
def order_detail(request, order_number):
    """Detalle de un pedido"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    context = {
        'order': order,
    }
    
    return render(request, 'order_detail.html', context)


@login_required
def cancel_order(request, order_number):
    """Cancelar un pedido"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    if not order.is_cancellable:
        messages.error(request, 'Este pedido no puede ser cancelado')
        return redirect('orders:order_detail', order_number=order_number)
    
    order.status = 'cancelled'
    order.save()
    
    messages.success(request, 'Pedido cancelado exitosamente')
    return redirect('orders:order_detail', order_number=order_number)


@login_required
def wishlist(request):
    """Lista de deseos del usuario"""
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    
    context = {
        'wishlist_items': wishlist_items,
    }
    
    return render(request, 'wishlist.html', context)


@login_required
def add_to_wishlist(request, product_slug):
    """Agregar producto a la lista de deseos"""
    product = get_object_or_404(Product, slug=product_slug, status='active')
    
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )
    
    if created:
        messages.success(request, f'{product.name} agregado a tu lista de deseos')
    else:
        messages.info(request, f'{product.name} ya está en tu lista de deseos')
    
    return redirect('products:product_detail', category_slug=product.category.slug, product_slug=product_slug)


@login_required
def remove_from_wishlist(request, item_id):
    """Remover producto de la lista de deseos"""
    wishlist_item = get_object_or_404(Wishlist, id=item_id, user=request.user)
    product_name = wishlist_item.product.name
    wishlist_item.delete()
    
    messages.success(request, f'{product_name} removido de tu lista de deseos')
    return redirect('orders:wishlist')


@login_required
def contact_info(request):
    """Vista para información de contacto"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product').all()
    cart_total = sum(item.total_price for item in cart_items)
    
    if request.method == 'POST':
        # Guardar información de contacto en la sesión
        request.session['contact_info'] = {
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
        }
        return redirect('orders:checkout')
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    
    return render(request, 'contact_info.html', context)
