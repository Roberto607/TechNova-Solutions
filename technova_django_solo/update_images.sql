"""
Script SQL para actualizar las rutas de imágenes de productos
"""

-- Actualizar iPhone 17 Pro Max
UPDATE products_product 
SET primary_image = 'products/primary/iphone-17-pro/iphone_imagen.jpg'
WHERE slug = 'iphone-17-pro-max';

-- Verificar actualización
SELECT id, name, slug, primary_image FROM products_product WHERE slug = 'iphone-17-pro-max';
