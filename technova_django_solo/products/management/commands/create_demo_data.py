from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.utils import timezone
from datetime import timedelta
import random

from products.models import Category, Product, Offer


class Command(BaseCommand):
    help = 'Create demo categories, products and offers for development'

    def handle(self, *args, **options):
        self.stdout.write('Creating demo categories...')

        category_names = [
            'Smartphones', 'Laptops', 'Tablets', 'Accesorios',
            'Audio', 'Cámaras', 'Monitores', 'Gaming'
        ]

        categories = []
        for name in category_names:
            slug = slugify(name)
            cat, created = Category.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': name,
                    'description': f'Demo category for {name}',
                    'is_active': True,
                }
            )
            categories.append(cat)
            if created:
                self.stdout.write(f'  - Created category: {name}')

        self.stdout.write('Creating demo products...')
        brands = ['TechNova', 'ElectroMax', 'GigaTech', 'NovaSound']

        created_products = 0
        for cat in categories:
            for i in range(1, 6):
                name = f"{cat.name} {i}"
                slug = slugify(f"{name}-{i}")
                price = round(random.uniform(49.99, 1999.99), 2)
                # Make some items on sale
                if random.choice([True, False]):
                    compare_at = round(price * random.uniform(1.05, 1.4), 2)
                else:
                    compare_at = None

                product, created = Product.objects.get_or_create(
                    slug=slug,
                    defaults={
                        'name': name,
                        'description': f'Demo description for {name}',
                        'short_description': f'Short desc {name}',
                        'category': cat,
                        'brand': random.choice(brands),
                        'model': f'Model-{random.randint(100,999)}',
                        'sku': f'SKU-{random.randint(100000,999999)}',
                        'price': price,
                        'compare_at_price': compare_at,
                        'stock_quantity': random.randint(0, 50),
                        'status': 'active',
                        'specifications': {'demo_spec': 'value'},
                        'features': ['Feature A', 'Feature B'],
                        'published_at': timezone.now(),
                    }
                )
                if created:
                    created_products += 1

        self.stdout.write(f'Created {created_products} new products')

        self.stdout.write('Creating demo offers...')
        now = timezone.now()
        offers_data = [
            {'title': 'Holiday Sale', 'discount_percentage': 20, 'price': 0},
            {'title': 'Clearance', 'discount_percentage': 35, 'price': 0},
            {'title': 'Flash Deal', 'discount_percentage': 10, 'price': 0},
        ]

        created_offers = 0
        for idx, od in enumerate(offers_data):
            start = now - timedelta(days=3)
            end = now + timedelta(days=15 + idx)
            offer, created = Offer.objects.get_or_create(
                title=od['title'],
                defaults={
                    'description': f'Demo offer: {od["title"]}',
                    'discount_percentage': od['discount_percentage'],
                    'start_date': start,
                    'end_date': end,
                    'is_active': True,
                }
            )
            if created:
                created_offers += 1

        self.stdout.write(f'Created {created_offers} offers')

        self.stdout.write(self.style.SUCCESS('Demo data creation complete.'))
