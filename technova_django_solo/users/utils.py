from datetime import timedelta
from django.utils import timezone
import uuid

def generate_verification_token():
    """Generar un token único para verificación de email"""
    return str(uuid.uuid4())

def get_verification_token_expiry():
    """Obtener fecha de expiración para el token (24 horas)"""
    return timezone.now() + timedelta(hours=24)
