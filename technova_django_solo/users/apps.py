"""
Users app configuration
Configuración de la aplicación users para gestión de usuarios
"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'Gestión de Usuarios'
    
    def ready(self):
        import users.signals