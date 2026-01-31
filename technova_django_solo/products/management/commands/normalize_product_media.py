from django.core.management.base import BaseCommand
from django.conf import settings
from products.models import Product, ProductImage
import os
import shutil


class Command(BaseCommand):
    help = 'Normalize product media into products/<product_id>/{primary,gallery}/ and update DB paths where possible.'

    def handle(self, *args, **options):
        moved = 0
        skipped = 0
        errors = 0

        self.stdout.write('Normalizing product media layout...')

        # Handle primary images
        for product in Product.objects.all():
            try:
                if not product.primary_image:
                    skipped += 1
                    continue

                current_name = product.primary_image.name  # stored path in DB
                # If already in new layout, skip
                expected_prefix = os.path.join('products', str(product.id))
                if current_name and current_name.startswith(expected_prefix):
                    skipped += 1
                    continue

                old_abs = os.path.join(settings.MEDIA_ROOT, current_name)
                filename = os.path.basename(current_name)
                new_rel = os.path.join('products', str(product.id), 'primary', filename)
                new_abs = os.path.join(settings.MEDIA_ROOT, new_rel)

                # If file exists at current path, move it
                if os.path.exists(old_abs):
                    os.makedirs(os.path.dirname(new_abs), exist_ok=True)
                    shutil.move(old_abs, new_abs)
                    product.primary_image.name = new_rel.replace('\\', '/')
                    product.save(update_fields=['primary_image'])
                    moved += 1
                    self.stdout.write(self.style.SUCCESS(f'Product {product.id}: moved {current_name} -> {new_rel}'))
                    continue

                # If not found, try the common old location 'products/primary/<slug>/'
                alt_old = os.path.join(settings.MEDIA_ROOT, 'products', 'primary', product.slug, filename)
                if os.path.exists(alt_old):
                    os.makedirs(os.path.dirname(new_abs), exist_ok=True)
                    shutil.move(alt_old, new_abs)
                    product.primary_image.name = new_rel.replace('\\', '/')
                    product.save(update_fields=['primary_image'])
                    moved += 1
                    self.stdout.write(self.style.SUCCESS(f'Product {product.id}: moved {alt_old} -> {new_rel}'))
                    continue

                self.stderr.write(self.style.WARNING(f'Product {product.id}: file not found for {current_name}'))
                errors += 1
            except Exception as e:
                errors += 1
                self.stderr.write(self.style.ERROR(f'Error processing primary image for product {product.id}: {e}'))

        # Handle gallery images
        for img in ProductImage.objects.all():
            try:
                current_name = img.image.name
                expected_prefix = os.path.join('products', str(img.product.id))
                if current_name and current_name.startswith(expected_prefix):
                    skipped += 1
                    continue

                old_abs = os.path.join(settings.MEDIA_ROOT, current_name)
                filename = os.path.basename(current_name)
                new_rel = os.path.join('products', str(img.product.id), 'gallery', filename)
                new_abs = os.path.join(settings.MEDIA_ROOT, new_rel)

                if os.path.exists(old_abs):
                    os.makedirs(os.path.dirname(new_abs), exist_ok=True)
                    shutil.move(old_abs, new_abs)
                    img.image.name = new_rel.replace('\\', '/')
                    img.save(update_fields=['image'])
                    moved += 1
                    self.stdout.write(self.style.SUCCESS(f'Gallery {img.id}: moved {current_name} -> {new_rel}'))
                    continue

                # Try common old location 'products/gallery/<slug>/'
                alt_old = os.path.join(settings.MEDIA_ROOT, 'products', 'gallery', img.product.slug, filename)
                if os.path.exists(alt_old):
                    os.makedirs(os.path.dirname(new_abs), exist_ok=True)
                    shutil.move(alt_old, new_abs)
                    img.image.name = new_rel.replace('\\', '/')
                    img.save(update_fields=['image'])
                    moved += 1
                    self.stdout.write(self.style.SUCCESS(f'Gallery {img.id}: moved {alt_old} -> {new_rel}'))
                    continue

                self.stderr.write(self.style.WARNING(f'Gallery {img.id}: file not found for {current_name}'))
                errors += 1
            except Exception as e:
                errors += 1
                self.stderr.write(self.style.ERROR(f'Error processing gallery image {img.id}: {e}'))

        self.stdout.write(self.style.SUCCESS('Normalization complete'))
        self.stdout.write(self.style.SUCCESS(f'Moved: {moved}, Skipped: {skipped}, Errors: {errors}'))
