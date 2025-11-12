from django.urls import path
from . import views

app_name = 'users'


urlpatterns = [
    # URLs de autenticación
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('orders/', views.orders, name='orders'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('verify/<str:token>/', views.verify_email, name='verify'),
    path('resend-verification/', views.resend_verification, name='resend_verification'),
    path('registro-exitoso/', views.registration_success, name='registration_success'),

]
    
    # URLs del perfil
   # path('perfil/', views.profile_view, name='profile'),
    #path('perfil/editar/', views.edit_profile, name='edit_profile'),
    #path('perfil/cambiar-contrasena/', views.change_password, name='change_password'),
    
    # URLs de recuperación de contraseña
    #path('recuperar-contrasena/', views.password_reset_request, name='password_reset'),
    #path('recuperar-contrasena/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    #path('recuperar-contrasena/completado/', views.password_reset_complete, name='password_reset_complete'),


