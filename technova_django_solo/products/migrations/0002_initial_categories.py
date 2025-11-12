from django.db import migrations

def create_initial_categories(apps, schema_editor):
    Category = apps.get_model('products', 'Category')
    
    categories = [
        {'name': 'Smartphones', 'slug': 'smartphones'},
        {'name': 'Laptops', 'slug': 'laptops'},
        {'name': 'Tablets', 'slug': 'tablets'},
        {'name': 'Audio & Video', 'slug': 'audio-video'},
    ]
    
    for cat_data in categories:
        Category.objects.get_or_create(**cat_data)

def reverse_initial_categories(apps, schema_editor):
    Category = apps.get_model('products', 'Category')
    Category.objects.filter(
        slug__in=['smartphones', 'laptops', 'tablets', 'audio-video']
    ).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            create_initial_categories,
            reverse_initial_categories,
        ),
    ]
