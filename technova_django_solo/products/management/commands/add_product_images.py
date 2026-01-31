"""
Comando de gestión para agregar imágenes adicionales a productos
"""
from django.core.management.base import BaseCommand
from products.models import Product, ProductImage


class Command(BaseCommand):
    help = 'Agrega imágenes adicionales al iPhone 17 Pro Max'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Agregando imágenes adicionales...'))
        
        try:
            # Obtener el producto del iPhone
            iphone = Product.objects.get(slug='iphone-17-pro-max')
            
            # Imágenes adicionales a agregar
            additional_images = [
                {
                    'path': 'products/primary/iphone-17-pro/1200_900.jpeg',
                    'alt_text': 'iPhone 17 Pro Max - Vista frontal',
                    'sort_order': 1
                },
                {
                    'path': 'products/primary/iphone-17-pro/highlights_ios__empnwsdz698i_large.jpg',
                    'alt_text': 'iPhone 17 Pro Max - Características iOS',
                    'sort_order': 2
                },
                {
                    'path': 'products/primary/iphone-17-pro/iPhone-17-Pro-Max-release-date-price-and-features.jpg',
                    'alt_text': 'iPhone 17 Pro Max - Especificaciones',
                    'sort_order': 3
                }
            ]
            
            # Eliminar imágenes adicionales existentes (si las hay)
            deleted = ProductImage.objects.filter(product=iphone).delete()
            if deleted[0] > 0:
                self.stdout.write(f'  Eliminadas {deleted[0]} imágenes previas')
            
            # Agregar las nuevas imágenes
            created_count = 0
            for img_data in additional_images:
                ProductImage.objects.create(
                    product=iphone,
                    image=img_data['path'],
                    alt_text=img_data['alt_text'],
                    sort_order=img_data['sort_order']
                )
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ {img_data["alt_text"]}'))
            
            self.stdout.write(self.style.SUCCESS(
                f'\n✓ Se agregaron {created_count} imágenes adicionales al {iphone.name}'
            ))
            
        except Product.DoesNotExist:
            self.stdout.write(self.style.ERROR('✗ Producto iPhone 17 Pro Max no encontrado'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error: {str(e)}'))
