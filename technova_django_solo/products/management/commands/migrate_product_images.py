"""
This management command was removed/replaced as requested by the developer.

If you need to migrate existing files to the new layout, implement a small
script that moves files from your current `media/` layout into the new
`products/<product_id>/{primary,gallery}/` layout and update the DB paths.

For now this command does nothing to avoid accidental execution.
"""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Disabled placeholder: migration handled manually or by a different tool.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('migrate_product_images command is disabled.'))
