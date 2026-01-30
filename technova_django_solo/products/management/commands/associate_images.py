import os
from django.core.management.base import BaseCommand
from django.conf import settings
from products.models import Product


class Command(BaseCommand):
    help = 'Associate existing files in media/products/primary to Product.primary_image when missing.'

    def handle(self, *args, **options):
        media_root = settings.MEDIA_ROOT
        base_dir = os.path.join(media_root, 'products', 'primary')
        if not os.path.isdir(base_dir):
            self.stdout.write('No media/products/primary directory found')
            return

        products = Product.objects.filter(primary_image='') | Product.objects.filter(primary_image__isnull=True)
        products = products.order_by('id')
        updated = 0
        for p in products:
            # Try exact slug folder
            candidate = None
            slug_folder = os.path.join(base_dir, p.slug)
            if os.path.isdir(slug_folder):
                files = [f for f in os.listdir(slug_folder) if not f.startswith('.')]
                if files:
                    candidate = os.path.join('products', 'primary', p.slug, files[0])

            # Try category folder
            if not candidate:
                cat_folder = os.path.join(base_dir, p.category.slug)
                if os.path.isdir(cat_folder):
                    files = [f for f in os.listdir(cat_folder) if not f.startswith('.')]
                    if files:
                        candidate = os.path.join('products', 'primary', p.category.slug, files[0])

            # Fallback: try any folder containing category name
            if not candidate:
                for dirname in os.listdir(base_dir):
                    if p.category.slug in dirname:
                        folder = os.path.join(base_dir, dirname)
                        if os.path.isdir(folder):
                            files = [f for f in os.listdir(folder) if not f.startswith('.')]
                            if files:
                                candidate = os.path.join('products', 'primary', dirname, files[0])
                                break

            if candidate:
                # assign to product.primary_image (Django stores the relative path)
                p.primary_image.name = candidate
                p.save(update_fields=['primary_image'])
                updated += 1
                self.stdout.write(f'Assigned image for product {p.id} "{p.name}": {candidate}')

        self.stdout.write(self.style.SUCCESS(f'Association complete: {updated} products updated.'))
