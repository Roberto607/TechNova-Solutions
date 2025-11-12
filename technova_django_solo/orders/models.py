"""
Orders app models
Modelos para gestión de pedidos, carritos y listas de deseos
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid


def generate_order_number():
    return f"TN{uuid.uuid4().hex[:10].upper()}"


def get_order_item_image_path(instance, filename):
    return f'order_items/{instance.order.order_number}/{filename}'


def default_shipping_address():
    return {}


def default_billing_address():
    return {}


class Wishlist(models.Model):
    """Lista de deseos del usuario"""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'product']
        verbose_name = "Lista de Deseos"
        verbose_name_plural = "Listas de Deseos"

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class Cart(models.Model):
    """Carrito de compras"""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True, related_name='carts')
    session_id = models.CharField(max_length=40, null=True, blank=True, help_text="Para usuarios no registrados")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"Carrito de {self.user.username}"
        return f"Carrito (sesión: {self.session_id})"


class CartItem(models.Model):
    """Items del carrito"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} en {self.cart}"
    
    @property
    def total_price(self):
        return self.product.price * self.quantity
    
    @property
    def total_savings(self):
        if self.product.is_on_sale:
            return (self.product.compare_at_price - self.product.price) * self.quantity
        return 0


class Order(models.Model):
    """Pedidos"""
    
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('confirmed', 'Confirmado'),
        ('processing', 'Procesando'),
        ('shipped', 'Enviado'),
        ('delivered', 'Entregado'),
        ('cancelled', 'Cancelado'),
        ('refunded', 'Reembolsado'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('paid', 'Pagado'),
        ('failed', 'Fallido'),
        ('refunded', 'Reembolsado'),
        ('partially_refunded', 'Parcialmente Reembolsado'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Tarjeta de Crédito'),
        ('debit_card', 'Tarjeta de Débito'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Transferencia Bancaria'),
        ('cash_on_delivery', 'Contra Entrega'),
    ]
    
    order_number = models.CharField(max_length=20, unique=True, default=generate_order_number)
    user = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='orders')
    
    # Información de contacto
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Direcciones
    shipping_address = models.JSONField(default=default_shipping_address, help_text="Información de dirección de envío")
    billing_address = models.JSONField(default=default_billing_address, help_text="Información de dirección de facturación")
    
    # Estados
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    
    # Totales
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Información adicional
    notes = models.TextField(blank=True)
    tracking_number = models.CharField(max_length=100, blank=True)
    
    # Fechas
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['user', 'status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Orden {self.order_number} - {self.user.username}"
    
    @property
    def is_completed(self):
        return self.status in ['delivered', 'refunded']
    
    @property
    def is_cancellable(self):
        return self.status in ['pending', 'confirmed']


class OrderItem(models.Model):
    """Items de pedidos"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT)
    
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Información del producto al momento de la compra (para historial)
    product_name = models.CharField(max_length=200)
    product_sku = models.CharField(max_length=50, blank=True)
    product_image = models.ImageField(upload_to=get_order_item_image_path, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity}x {self.product_name}"
    
    def save(self, *args, **kwargs):
        # Guardar información del producto al momento de la compra
        if not self.product_name:
            self.product_name = self.product.name
        if not self.product_sku:
            self.product_sku = self.product.sku or ''
        if not self.product_image and self.product.primary_image:
            self.product_image = self.product.primary_image
            
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)
