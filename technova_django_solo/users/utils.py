import uuid
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
import secrets
import string

def generate_verification_token():
    """Generar un token único para verificación de email"""
    return uuid.uuid4().hex

def generate_password_reset_token():
    """Generar un token único para reset de contraseña"""
    return secrets.token_urlsafe(32)

def get_verification_token_expiry():
    """Obtener fecha de expiración para el token (24 horas)"""
    return timezone.now() + timedelta(hours=24)

def get_password_reset_expiry():
    """Obtener fecha de expiración para el token de reset (1 hora)"""
    return timezone.now() + timedelta(hours=1)

def generate_random_password(length=12):
    """Generar una contraseña aleatoria segura"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

def verify_token_format(token):
    """Verificar que el token tenga el formato correcto"""
    try:
        uuid.UUID(token)
        return True
    except ValueError:
        return False

