"""
Script para agregar imágenes adicionales al iPhone 17 Pro Max
"""
from products.models import Product, ProductImage

# Obtener el producto del iPhone
try:
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
    ProductImage.objects.filter(product=iphone).delete()
    
    # Agregar las nuevas imágenes
    for img_data in additional_images:
        ProductImage.objects.create(
            product=iphone,
            image=img_data['path'],
            alt_text=img_data['alt_text'],
            sort_order=img_data['sort_order']
        )
        print(f'✓ Agregada imagen: {img_data["alt_text"]}')
    
    print(f'\n✓ Se agregaron {len(additional_images)} imágenes adicionales al {iphone.name}')
    
except Product.DoesNotExist:
    print('✗ Producto iPhone 17 Pro Max no encontrado')
except Exception as e:
    print(f'✗ Error: {str(e)}')
