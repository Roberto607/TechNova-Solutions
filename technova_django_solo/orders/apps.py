"""
Orders app configuration
Configuración de la aplicación orders para gestión de pedidos
"""

from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'
    verbose_name = 'Gestión de Pedidos'
    
    def ready(self):
        import orders.signals