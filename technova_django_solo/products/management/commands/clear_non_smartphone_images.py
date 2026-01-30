from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = 'Clear primary_image for all products whose category slug is not smartphones'

    def handle(self, *args, **options):
        qs = Product.objects.exclude(category__slug__iexact='smartphones').exclude(primary_image__isnull=True).exclude(primary_image='')
        total = qs.count()
        for p in qs:
            p.primary_image.delete(save=False)
            p.primary_image = None
            p.save(update_fields=['primary_image'])
            self.stdout.write(f'Cleared image for product id={p.id} name="{p.name}"')

        self.stdout.write(self.style.SUCCESS(f'Cleared primary_image for {total} non-smartphone products'))
