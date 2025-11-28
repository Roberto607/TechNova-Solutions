"""
Management command para crear ofertas de prueba
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from products.models import Offer


class Command(BaseCommand):
    help = 'Crea ofertas de prueba para el sistema de promociones'

    def handle(self, *args, **kwargs):
        # Limpiar ofertas antiguas (opcional)
        self.stdout.write('Creando ofertas de prueba...')
        
        now = timezone.now()
        
        offers_data = [
            {
                'title': '🔥 iPhone 15 Pro Max - Oferta Especial',
                'description': '¡Ahorra hasta $300 en el último iPhone! Incluye AirPods gratis con tu compra.',
                'discount_percentage': 25,
                'price': 1299.99,
                'start_date': now - timedelta(days=1),
                'end_date': now + timedelta(days=30),
                'is_active': True
            },
            {
                'title': '💻 MacBook Pro M3 - Precio Increíble',
                'description': 'La mejor laptop para profesionales creativos. Descuento exclusivo por tiempo limitado.',
                'discount_percentage': 15,
                'price': 2499.99,
                'start_date': now - timedelta(hours=5),
                'end_date': now + timedelta(days=15),
                'is_active': True
            },
            {
                'title': '🎧 Sony WH-1000XM5 - Black Friday',
                'description': 'Los mejores audífonos con cancelación de ruido del mercado. ¡Oferta limitada!',
                'discount_percentage': 30,
                'price': 399.99,
                'start_date': now - timedelta(hours=2),
                'end_date': now + timedelta(days=7),
                'is_active': True
            },
            {
                'title': '⚡ Samsung Galaxy S24 Ultra - Envío Gratis',
                'description': 'El smartphone más potente de Samsung. Incluye funda y protector de pantalla gratis.',
                'discount_percentage': 20,
                'price': 1199.99,
                'start_date': now,
                'end_date': now + timedelta(days=20),
                'is_active': True
            },
            {
                'title': '🖥️ iPad Pro 12.9" - Promoción Especial',
                'description': 'Perfecta para diseñadores y estudiantes. Apple Pencil incluido en la compra.',
                'discount_percentage': 18,
                'price': 1099.99,
                'start_date': now - timedelta(hours=3),
                'end_date': now + timedelta(days=25),
                'is_active': True
            }
        ]
        
        created_count = 0
        for offer_data in offers_data:
            offer, created = Offer.objects.get_or_create(
                title=offer_data['title'],
                defaults=offer_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Oferta creada: {offer.title}')
                )
            else:
                # Actualizar si ya existe
                for key, value in offer_data.items():
                    setattr(offer, key, value)
                offer.save()
                self.stdout.write(
                    self.style.WARNING(f'↻ Oferta actualizada: {offer.title}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Proceso completado: {created_count} ofertas nuevas creadas')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Total de ofertas activas: {Offer.objects.filter(is_active=True).count()}')
        )
