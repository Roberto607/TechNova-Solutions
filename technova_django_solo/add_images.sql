-- Script SQL para agregar imágenes adicionales del iPhone 17 Pro Max
INSERT INTO products_productimage (product_id, image, alt_text, sort_order, created_at) 
VALUES 
(1, 'products/primary/iphone-17-pro/1200_900.jpeg', 'iPhone 17 Pro Max - Vista frontal', 1, datetime('now')),
(1, 'products/primary/iphone-17-pro/highlights_ios__empnwsdz698i_large.jpg', 'iPhone 17 Pro Max - Características iOS', 2, datetime('now')),
(1, 'products/primary/iphone-17-pro/iPhone-17-Pro-Max-release-date-price-and-features.jpg', 'iPhone 17 Pro Max - Especificaciones', 3, datetime('now'));

-- Verificar las imágenes insertadas
SELECT id, product_id, image, alt_text, sort_order FROM products_productimage WHERE product_id = 1;
