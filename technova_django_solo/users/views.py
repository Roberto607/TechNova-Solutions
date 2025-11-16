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
User = get_user_model()


@csrf_protect
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
            
            # Preparar contexto para el email
            context = {
                'user': user,
                'verification_url': f"{settings.SITE_URL}/usuarios/verify/{token}",
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
            
            return redirect('users:registration_success')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form})

                
def registration_success(request):
    """Vista que muestra el mensaje de registro exitoso"""
    return render(request, 'registration_success.html')
                
def verify_email(request, token):
    """Verificar email del usuario"""
    try:
        verification_token = VerificationToken.objects.get(token=token)
        if verification_token.is_valid():
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
            messages.error(request, 'El enlace de verificación ha expirado. Por favor, solicita uno nuevo.')
            return redirect('users:register')
    except VerificationToken.DoesNotExist:
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
                'verification_url': f"{settings.SITE_URL}/usuarios/verificar/{token}/",
            }
            
            # Renderizar template HTML
            html_content = render_to_string('users/verification_email.html', context)
            
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

def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión exitosamente.")
    return redirect('core:home')



def orders(request):
    return render(request, 'orders.html')

def wishlist(request):
    return render(request, 'wishlist.html')


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
    }
    
    return render(request, 'dashboard.html', context)
