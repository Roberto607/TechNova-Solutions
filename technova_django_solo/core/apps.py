"""
Core app configuration
Configuración de la aplicación core para funcionalidades centrales
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'Funcionalidades Centrales'
    
    def ready(self):
        import core.signals