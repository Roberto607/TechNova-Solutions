"""
Products app configuration
Configuración de la aplicación products para gestión de productos
"""

from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
    verbose_name = 'Gestión de Productos'
    
    def ready(self):
        import products.signals