from django.core.management.base import BaseCommand
from products.models import Category, Product


class Command(BaseCommand):
    help = 'Inspect laptop products and print slug and primary_image info'

    def handle(self, *args, **options):
        try:
            cat = Category.objects.filter(slug__icontains='laptop')
            if not cat.exists():
                self.stdout.write('No category with slug containing "laptop" found')
                return
            for c in cat:
                self.stdout.write(f'Category: {c.name} (slug={c.slug})')
                qs = Product.objects.filter(category=c)
                if not qs.exists():
                    self.stdout.write('  No products in this category')
                    continue
                for p in qs:
                    pi = p.primary_image
                    self.stdout.write(f'  Product id={p.id} name="{p.name}" slug="{p.slug}" primary_image={getattr(pi, "name", None)}')
        except Exception as e:
            self.stdout.write(f'Error: {e}')
