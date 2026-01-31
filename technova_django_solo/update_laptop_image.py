import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Actualizar la imagen del laptop
cursor.execute(
    "UPDATE products_product SET primary_image = ? WHERE slug = ?",
    ('products/primary/laptops/photo_2025-11-11_00-47-17.jpg', 'laptp')
)
conn.commit()

# Verificar
cursor.execute('SELECT id, name, slug, primary_image FROM products_product')
rows = cursor.fetchall()

print('Productos actualizados:\n')
for row in rows:
    print(f'ID: {row[0]}')
    print(f'  Name: {row[1]}')
    print(f'  Slug: {row[2]}')
    print(f'  Image: {row[3]}\n')

conn.close()
print('✓ Actualización completada!')
