import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Normalizar las rutas (convertir \ a /)
cursor.execute(
    "UPDATE products_product SET primary_image = REPLACE(primary_image, '\\', '/') WHERE primary_image IS NOT NULL"
)
conn.commit()

# Verificar
cursor.execute('SELECT id, name, slug, primary_image FROM products_product')
rows = cursor.fetchall()

print('Rutas normalizadas:\n')
for row in rows:
    print(f'ID: {row[0]}')
    print(f'  Name: {row[1]}')
    print(f'  Slug: {row[2]}')
    print(f'  Image: {row[3]}\n')

conn.close()
print('✓ Normalización completada!')
