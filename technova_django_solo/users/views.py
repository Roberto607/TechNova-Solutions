from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegistrationForm
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from .models import VerificationToken
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
import uuid
from django.template.loader import render_to_string
from django.utils import timezone
from orders.models import Order
from orders.models import Wishlist
from django.core.paginator import Paginator
User = get_user_model()
from django.urls import reverse


from .forms import UserRegistrationForm, UserUpdateForm, UserProfileForm


@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                print(f"Usuario autenticado: {user.username}")
                print(f"Is superuser: {user.is_superuser}")
                print(f"Is staff: {user.is_staff}")
                
                login(request, user)
                print("Login exitoso")
                
                # Verificar después del login
                print(f"Después del login - Is superuser: {request.user.is_superuser}")
                print(f"Después del login - Is staff: {request.user.is_staff}")
                
                messages.success(request, f'¡Bienvenido {username}!')
                
                if user.is_superuser or user.is_staff:
                    print("Redirigiendo al panel de administración")
                    return redirect('admin_panel:admin_dashboard')
                else:
                    print("Redirigiendo al home")
                    return redirect('core:home')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
        else:
            messages.error(request, 'Por favor, corrige los errores del formulario')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})








@csrf_protect
def register_view(request):
    """Vista de registro con email HTML"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            # Crear token de verificación
            token = str(uuid.uuid4())
            VerificationToken.objects.create(
                user=user,
                token=token,
                expires_at=timezone.now() + timezone.timedelta(hours=24)
            )
            
            # Preparar contexto para el email (usar URL absoluta desde la request)
            verification_url = request.build_absolute_uri(reverse('users:verify', args=[token]))
            print(f"URL de verificación: {verification_url}")  # Debug
            print(f"SITE_URL: {settings.SITE_URL}")  # Debug
            print(f"Token: {token}")  # Debug
            
            context = {
                'user': user,
                'verification_url': verification_url,
            }
            
            print(f"Contexto del email: {context}")  # Debug
            
            # Renderizar template HTML
            html_content = render_to_string('verification_email.html', context)
            
            # Crear y enviar email
            email = EmailMessage(
                subject='Verifica tu cuenta de TechNova Solutions',
                body=html_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            email.content_subtype = "html"
            
            try:
                result = email.send()
                print(f"Resultado del envío: {result}")  # Debug
                messages.success(request, 'Se ha enviado un email de verificación.')
                return redirect('users:registration_success')
            except Exception as e:
                print(f"Error al enviar email: {str(e)}")  # Debug
                messages.error(request, f'Error al enviar el email: {str(e)}')
                user.delete()  # Eliminar el usuario si el email no se pudo enviar
                return redirect('users:register')
        else:
            messages.error(request, 'Por favor, corrige los errores del formulario')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form})


def verify_email(request, token):
    """Verificar email del usuario"""
    print(f"Token recibido: {token}")  # Debug
    
    try:
        verification_token = VerificationToken.objects.get(token=token)
        print(f"Token encontrado: {verification_token}")  # Debug
        print(f"Válido hasta: {verification_token.expires_at}")  # Debug
        
        if verification_token.is_valid():
            print("Token válido")  # Debug
            user = verification_token.user
            user.is_active = True
            user.save()
            verification_token.delete()
            
            # Especificar el backend de autenticación
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            
            messages.success(request, '¡Tu cuenta ha sido verificada! Bienvenido a TechNova Solutions.')
            return redirect('core:home')
        else:
            print("Token inválido o expirado")  # Debug
            messages.error(request, 'El enlace de verificación ha expirado. Por favor, solicita uno nuevo.')
            return redirect('users:register')
    except VerificationToken.DoesNotExist:
        print("Token no existe en la base de datos")  # Debug
        messages.error(request, 'Enlace de verificación inválido.')
        return redirect('users:register')


def resend_verification(request):
    """Reenviar email de verificación"""
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email, is_active=False)
            
            # Crear nuevo token
            token = str(uuid.uuid4())
            VerificationToken.objects.create(
                user=user,
                token=token,
                expires_at=timezone.now() + timezone.timedelta(hours=24)
            )
            
            # Preparar contexto para el email
            context = {
                'user': user,
                'verification_url': request.build_absolute_uri(reverse('users:verify', args=[token])),
            }
            
            # Renderizar template HTML
            html_content = render_to_string('verification_email.html', context)
            
            # Crear y enviar email
            email = EmailMessage(
                subject='Verifica tu cuenta de TechNova Solutions',
                body=html_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            email.content_subtype = "html"
            email.send()
            
            messages.success(request, 'Se ha enviado un nuevo email de verificación.')
            return redirect('users:login')
            
        except User.DoesNotExist:
            messages.error(request, 'No existe una cuenta con ese email o ya está verificada.')
            return redirect('users:register')
    
    return render(request, 'resend_verification.html')

def registration_success(request):
    """Vista que muestra el mensaje de registro exitoso"""
    return render(request, 'registration_success.html')
def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión exitosamente.")
    return redirect('core:home')



def orders(request):
    # Mostrar lista de pedidos dentro del panel 'Mi Cuenta'
    if not request.user.is_authenticated:
        return redirect('users:login')

    orders_qs = Order.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(orders_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'orders': page_obj,
        'page_obj': page_obj,
        'active_tab': 'orders',
    }

    return render(request, 'orders.html', context)

def wishlist(request):
    # Render wishlist within Mi Cuenta to keep consistent menu
    if not request.user.is_authenticated:
        return redirect('users:login')

    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')

    context = {
        'wishlist_items': wishlist_items,
        'active_tab': 'wishlist',
    }

    return render(request, 'wishlist.html', context)


@login_required
def dashboard_view(request):
    """Vista del dashboard del usuario"""
    # Obtener datos del usuario
    orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')[:5]
    
    context = {
        'user': request.user,
        'recent_orders': orders,
        'wishlist_count': Wishlist.objects.filter(user=request.user).count(),
        'recent_wishlist': wishlist_items,
        'active_tab': 'dashboard',
    }
    
    return render(request, 'dashboard.html', context)


@login_required
def edit_profile(request):
    """Editar información básica y perfil del usuario dentro de Mi Cuenta"""
    user = request.user

    try:
        profile = user.profile
    except Exception:
        from .models import UserProfile
        profile = UserProfile.objects.create(user=user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Perfil actualizado correctamente')
            return redirect('users:dashboard')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'active_tab': 'dashboard',
    }

    return render(request, 'edit_profile.html', context)
