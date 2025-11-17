"""
Products app models
Modelos para gestión de productos y categorías
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid


def get_product_image_path(instance, filename):
    return f'products/primary/{instance.slug}/{filename}'


def get_category_image_path(instance, filename):
    return f'categories/{instance.slug}/{filename}'


def get_product_gallery_path(instance, filename):
    return f'products/gallery/{instance.product.slug}/{filename}'


def default_specifications():
    return {}


def default_features():
    return []


class Category(models.Model):
    """Categorías de productos"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to=get_category_image_path, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    is_active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.name


class Product(models.Model):
    """Modelo de productos"""
    
    CONDITION_CHOICES = [
        ('new', 'Nuevo'),
        ('refurbished', 'Reacondicionado'),
        ('used', 'Usado'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Activo'),
        ('inactive', 'Inactivo'),
        ('out_of_stock', 'Agotado'),
        ('discontinued', 'Descontinuado'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    brand = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    sku = models.CharField(max_length=50, unique=True, null=True, blank=True)
    
    # Precios
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    compare_at_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    
    # Inventario
    stock_quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    low_stock_threshold = models.IntegerField(default=10, validators=[MinValueValidator(0)])
    
    # Especificaciones técnicas
    specifications = models.JSONField(default=default_specifications, blank=True, help_text="Especificaciones técnicas en formato JSON")
    features = models.JSONField(default=default_features, blank=True, help_text="Lista de características")
    
    # Imágenes
    primary_image = models.ImageField(upload_to=get_product_image_path, blank=True, null=True)
    
    # Propiedades del producto
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='new')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    dimensions = models.CharField(max_length=100, blank=True, help_text="Largo x Ancho x Alto en cm")
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)
    meta_keywords = models.CharField(max_length=500, blank=True)
    
    # Rating y reviews
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    review_count = models.IntegerField(default=0)
    
    # Fechas
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['price']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.name} ({self.brand})"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('product_detail', args=[self.category.slug, self.slug])
    
    @property
    def is_on_sale(self):
        return self.compare_at_price and self.compare_at_price > self.price
    
    @property
    def discount_percentage(self):
        if self.is_on_sale:
            return int(((self.compare_at_price - self.price) / self.compare_at_price) * 100)
        return 0
    
    @property
    def is_low_stock(self):
        return self.stock_quantity <= self.low_stock_threshold
    
    @property
    def is_out_of_stock(self):
        return self.stock_quantity == 0


class ProductImage(models.Model):
    """Imágenes adicionales de productos"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to=get_product_gallery_path)
    alt_text = models.CharField(max_length=200, blank=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order']
        verbose_name = "Imagen de Producto"
        verbose_name_plural = "Imágenes de Productos"

    def __str__(self):
        return f"Imagen de {self.product.name}"


class Review(models.Model):
    """Reseñas de productos"""
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='reviews')
    order_item = models.ForeignKey('orders.OrderItem', on_delete=models.CASCADE, null=True, blank=True)
    
    rating = models.IntegerField(choices=RATING_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200, blank=True)
    comment = models.TextField()
    
    is_verified_purchase = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['product', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f"Reseña de {self.user.username} para {self.product.name}"
    
    
class Offer(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='offers/', blank=True, null=True)  # Añade blank=True, null=True
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    start_date = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    @property
    def final_price(self):
        """Calcula el precio final con descuento"""
        if self.discount_percentage and self.price:
            discount = self.price * (self.discount_percentage / 100)
            return self.price - discount
        return self.price
