"""
Script de gestión para sincronizar imágenes de productos con la base de datos
"""
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from products.models import Product


class Command(BaseCommand):
    help = 'Sincroniza las imágenes de productos del directorio media con la base de datos'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Iniciando sincronización de imágenes...'))
        
        # Directorio donde están las imágenes
        products_dir = os.path.join(settings.MEDIA_ROOT, 'products', 'primary')
        
        if not os.path.exists(products_dir):
            self.stdout.write(self.style.ERROR(f'El directorio {products_dir} no existe'))
            return
        
        # Listar todos los subdirectorios (cada uno representa un producto)
        product_folders = [f for f in os.listdir(products_dir) 
                          if os.path.isdir(os.path.join(products_dir, f))]
        
        self.stdout.write(f'Encontrados {len(product_folders)} directorios de productos')
        
        updated_count = 0
        not_found_count = 0
        
        for folder in product_folders:
            folder_path = os.path.join(products_dir, folder)
            
            # Buscar imágenes en el directorio
            image_files = [f for f in os.listdir(folder_path) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif'))]
            
            if not image_files:
                self.stdout.write(self.style.WARNING(f'  No se encontraron imágenes en {folder}'))
                continue
            
            # Tomar la primera imagen encontrada
            image_file = image_files[0]
            
            # Construir la ruta relativa desde MEDIA_ROOT
            relative_path = os.path.join('products', 'primary', folder, image_file)
            
            # Intentar encontrar el producto por diferentes criterios
            product = None
            
            # 1. Intentar por slug exacto
            try:
                product = Product.objects.get(slug=folder)
            except Product.DoesNotExist:
                pass
            
            # 2. Intentar por slug que contenga el nombre del folder
            if not product:
                try:
                    product = Product.objects.get(slug__istartswith=folder)
                except (Product.DoesNotExist, Product.MultipleObjectsReturned):
                    pass
            
            # 3. Intentar por slug que comience con partes del folder
            if not product:
                folder_parts = folder.split('-')
                for i in range(len(folder_parts), 0, -1):
                    partial_slug = '-'.join(folder_parts[:i])
                    try:
                        products = Product.objects.filter(slug__istartswith=partial_slug)
                        if products.count() == 1:
                            product = products.first()
                            break
                    except Product.DoesNotExist:
                        pass
            
            # 4. Intentar por nombre similar
            if not product:
                folder_name = folder.replace('-', ' ').replace('_', ' ')
                products = Product.objects.filter(name__icontains=folder_name)
                if products.count() == 1:
                    product = products.first()
            
            if product:
                # Actualizar la imagen del producto
                product.primary_image = relative_path
                product.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(
                    f'  ✓ {product.name}: {image_file}'
                ))
            else:
                not_found_count += 1
                self.stdout.write(self.style.ERROR(
                    f'  ✗ No se encontró producto para el directorio: {folder}'
                ))
        
        self.stdout.write(self.style.SUCCESS(
            f'\n✓ Sincronización completada: {updated_count} productos actualizados'
        ))
        if not_found_count > 0:
            self.stdout.write(self.style.WARNING(
                f'⚠ {not_found_count} directorios sin producto correspondiente'
            ))
