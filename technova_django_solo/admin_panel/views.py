from django.shortcuts import redirect,render
from django.contrib.auth.decorators import login_required, user_passes_test
from products.models import Product, Offer
from django.contrib.auth import get_user_model
from orders.models import Order
 # Obtener estadísticas
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .forms import ProductForm, UserForm
from django.contrib.auth.models import Group, Permission

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
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'admin_product_detail.html', {'product': product, 'title': 'Detalle Producto'})


@login_required
@user_passes_test(is_admin, login_url='/usuarios/login/')
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto añadido correctamente')
            return redirect('admin_panel:admin_products')
    else:
        form = ProductForm()
    return render(request, 'admin_product_form.html', {'form': form, 'title': 'Agregar Producto'})


@login_required
@user_passes_test(is_admin, login_url='/usuarios/login/')
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado')
            return redirect('admin_panel:admin_product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin_product_form.html', {'form': form, 'product': product, 'title': 'Editar Producto'})


@login_required
@user_passes_test(is_admin, login_url='/usuarios/login/')
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Producto eliminado')
        return redirect('admin_panel:admin_products')
    return render(request, 'admin_product_confirm_delete.html', {'product': product, 'title': 'Eliminar Producto'})

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
def offer_detail(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    return render(request, 'admin_offer_detail.html', {'offer': offer, 'title': 'Detalle Oferta'})


@login_required
@user_passes_test(is_admin, login_url='/usuarios/login/')
def offer_add(request):
    from .forms import OfferForm
    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Oferta creada')
            return redirect('admin_panel:admin_offers')
    else:
        form = OfferForm()
    return render(request, 'admin_offer_form.html', {'form': form, 'title': 'Agregar Oferta'})


@login_required
@user_passes_test(is_admin, login_url='/usuarios/login/')
def offer_edit(request, pk):
    from .forms import OfferForm
    offer = get_object_or_404(Offer, pk=pk)
    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES, instance=offer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Oferta actualizada')
            return redirect('admin_panel:admin_offer_detail', pk=offer.pk)
    else:
        form = OfferForm(instance=offer)
    return render(request, 'admin_offer_form.html', {'form': form, 'offer': offer, 'title': 'Editar Oferta'})


@login_required
@user_passes_test(is_admin, login_url='/usuarios/login/')
def offer_delete(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    if request.method == 'POST':
        offer.delete()
        messages.success(request, 'Oferta eliminada')
        return redirect('admin_panel:admin_offers')
    return render(request, 'admin_offer_confirm_delete.html', {'offer': offer, 'title': 'Eliminar Oferta'})

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
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'admin_user_detail.html', {'user_obj': user, 'title': 'Detalle Usuario'})


@login_required
@user_passes_test(is_admin, login_url='/usuarios/login/')
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado')
            return redirect('admin_panel:admin_user_detail', pk=user.pk)
    else:
        form = UserForm(instance=user)
    return render(request, 'admin_user_form.html', {'form': form, 'user_obj': user, 'title': 'Editar Usuario'})


@login_required
@user_passes_test(is_admin, login_url='/usuarios/login/')
def user_permissions(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        is_staff = request.POST.get('is_staff') == 'on'
        is_super = request.POST.get('is_superuser') == 'on'
        user.is_staff = is_staff
        user.is_superuser = is_super
        # groups
        group_ids = request.POST.getlist('groups')
        groups = Group.objects.filter(id__in=group_ids)
        user.groups.set(groups)
        user.save()
        messages.success(request, 'Permisos actualizados')
        return redirect('admin_panel:admin_user_detail', pk=user.pk)
    groups = Group.objects.all()
    permissions = Permission.objects.all()
    return render(request, 'admin_user_permissions.html', {'user_obj': user, 'groups': groups, 'permissions': permissions, 'title': 'Permisos Usuario'})

@login_required
@user_passes_test(is_admin, login_url='/usuarios/login/')
def orders(request):
    orders = Order.objects.all().order_by('-created_at')
    context = {
        'orders': orders,
        'title': 'Gestionar Pedidos',
    }
    return render(request, 'admin_orders.html', context)


@login_required
@user_passes_test(is_admin, login_url='/usuarios/login/')
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'admin_order_detail.html', {'order': order, 'title': 'Detalle Pedido'})


@login_required
@user_passes_test(is_admin, login_url='/usuarios/login/')
def order_update_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status:
            order.status = status
            order.save()
            messages.success(request, 'Estado del pedido actualizado')
            return redirect('admin_panel:admin_order_detail', pk=order.pk)
    return render(request, 'admin_order_update.html', {'order': order, 'title': 'Actualizar Pedido'})



