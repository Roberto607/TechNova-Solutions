"""
Script manual para asignar imágenes a productos específicos
Ejecuta este archivo con: python manage.py shell < fix_product_images.py
"""
import os
from products.models import Product

# Mapeo directo de slugs de productos a directorios de imágenes
mappings = {
    'iphone-17-pro-max': 'iphone-17-pro',
    'laptp': 'laptops',
    # Agrega más mappings según sea necesario
}

media_root = 'media'
updated = 0

for product_slug, folder_name in mappings.items():
    try:
        product = Product.objects.get(slug=product_slug)
        
        # Ruta completa al directorio de imágenes
        image_dir = os.path.join(media_root, 'products', 'primary', folder_name)
        
        if os.path.exists(image_dir):
            # Buscar la primera imagen en el directorio
            image_files = [f for f in os.listdir(image_dir) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif'))]
            
            if image_files:
                # Usar la primera imagen encontrada
                image_file = image_files[0]
                relative_path = f'products/primary/{folder_name}/{image_file}'
                
                product.primary_image = relative_path
                product.save()
                updated += 1
                
                print(f'✓ Actualizado: {product.name} -> {image_file}')
            else:
                print(f'✗ No se encontraron imágenes en: {image_dir}')
        else:
            print(f'✗ Directorio no existe: {image_dir}')
            
    except Product.DoesNotExist:
        print(f'✗ Producto no encontrado: {product_slug}')

print(f'\n{updated} productos actualizados')
