"""
Signals para la aplicación products
Maneja actualizaciones automáticas de productos
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg, Count
from .models import Review, Product


@receiver(post_save, sender=Review)
def update_product_rating(sender, instance, **kwargs):
    """Actualizar rating promedio del producto cuando se agrega/actualiza una review"""
    product = instance.product
    
    # Calcular nuevo promedio
    reviews = product.reviews.filter(is_approved=True)
    if reviews.exists():
        avg_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0
        review_count = reviews.count()
    else:
        avg_rating = 0
        review_count = 0
    
    # Actualizar producto
    Product.objects.filter(id=product.id).update(
        average_rating=avg_rating,
        review_count=review_count
    )


@receiver(post_delete, sender=Review)
def update_product_rating_on_delete(sender, instance, **kwargs):
    """Actualizar rating promedio cuando se elimina una review"""
    product = instance.product
    
    # Recalcular
    reviews = product.reviews.filter(is_approved=True)
    if reviews.exists():
        avg_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0
        review_count = reviews.count()
    else:
        avg_rating = 0
        review_count = 0
    
    # Actualizar producto
    Product.objects.filter(id=product.id).update(
        average_rating=avg_rating,
        review_count=review_count
    )