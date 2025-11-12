"""
Users app models
Modelos para gestión de usuarios y autenticación
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import uuid

class VerificationToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def is_valid(self):
        return timezone.now() < self.expires_at
    
    def __str__(self):
        return f"Token for {self.user.username}"

class UserProfile(models.Model):
    """Perfil extendido del usuario para información adicional"""
    USER_TYPE_CHOICES = [
        ('guest', 'Invitado'),
        ('registered', 'Registrado'),
        ('premium', 'Premium'),
        ('business', 'Empresarial'),
    ]
    
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='registered')
    phone = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ], blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    interests = models.TextField(blank=True, help_text="Intereses separados por comas")
    referral_source = models.CharField(max_length=100, blank=True, null=True)
    newsletter_subscription = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Perfil de {self.user.email}"


class User(AbstractUser):
    """Modelo de usuario personalizado para TechNova"""
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
