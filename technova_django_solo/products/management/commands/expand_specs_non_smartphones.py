from django.core.management.base import BaseCommand
from products.models import Product
from django.utils import timezone


EXTRA_SPECS = {
    'laptops': {
        'Connectivity': 'Wi-Fi 6, Bluetooth 5.2, USB-C/Thunderbolt',
        'Weight': '1.0 - 2.0 kg',
        'Dimensions': 'Approx. 300 x 215 x 15 mm',
        'Battery Life': '8-18 hours depending on usage',
        'Ports': 'USB-C, USB-A, HDMI (model-dependent)',
        'Warranty': '1 year (varía por región)'
    },
    'tablets': {
        'Connectivity': 'Wi-Fi 6 / LTE optional, Bluetooth 5.0',
        'Weight': '0.4 - 0.8 kg',
        'Dimensions': 'Approx. 250 x 175 x 7 mm',
        'Battery Life': '8-12 hours',
        'Accessories': 'Apple Pencil / S Pen compatibility (model-dependent)',
        'Warranty': '1 year'
    },
    'accesorios': {
        'Compatibility': 'Universal / Device-specific',
        'Materials': 'Plastic / Aluminum / Silicone',
        'Warranty': '1 year',
        'Connectivity': 'Bluetooth / Wired / USB-C'
    },
    'audio': {
        'Driver Size': '20-50 mm',
        'Impedance': '16-64 ohm',
        'Frequency Response': '20Hz - 20kHz',
        'Battery Life': '10-80 hours (wireless)',
        'Connectivity': 'Bluetooth / Wired / NFC'
    },
    'camaras': {
        'Sensor Type': 'Full-frame / APS-C / Micro Four Thirds',
        'Megapixels': '20-45 MP typical',
        'Video': '4K / 60p support (model-dependent)',
        'IBIS': 'Yes/No depending on model',
        'Lens Mount': 'RF / E / Z / F / Micro Four Thirds'
    },
    'monitores': {
        'Panel Type': 'IPS / VA / OLED',
        'Resolution': 'FHD / QHD / 4K',
        'Refresh Rate': '60-240Hz',
        'Ports': 'HDMI / DisplayPort / USB-C',
        'Color Gamut': 'sRGB / AdobeRGB / DCI-P3'
    },
    'gaming': {
        'Platform': 'PC / Console',
        'CPU/GPU': 'High-end CPUs and GPUs for gaming rigs',
        'Storage': 'SSD preferred for fast load times',
        'Cooling': 'Advanced cooling solutions',
        'Extras': 'RGB, mechanical keyboard, low-latency displays'
    }
}


class Command(BaseCommand):
    help = 'Expand specifications and features for non-smartphone products'

    def handle(self, *args, **options):
        qs = Product.objects.exclude(category__slug__iexact='smartphones')
        updated = 0
        for p in qs:
            cat_slug = p.category.slug.lower()
            extras = EXTRA_SPECS.get(cat_slug, {})
            # merge specs: keep existing and add extras if missing
            specs = p.specifications or {}
            for k, v in extras.items():
                if k not in specs:
                    specs[k] = v

            # add some generic metadata
            if 'Release Date' not in specs:
                specs['Release Date'] = str(timezone.now().date())
            if 'Warranty' not in specs:
                specs['Warranty'] = specs.get('Warranty', '1 year')

            p.specifications = specs

            # expand features list
            features = list(p.features or [])
            additions = []
            if cat_slug == 'laptops':
                additions = ['Backlit keyboard', 'Fast charging', 'Thunderbolt support', 'Fingerprint reader']
            elif cat_slug == 'tablets':
                additions = ['Stylus support', 'Docking keyboard compatible', 'Multi-window multitasking']
            elif cat_slug == 'accesorios':
                additions = ['Plug-and-play', 'Compact design', 'Durable build']
            elif cat_slug == 'audio':
                additions = ['Noise cancellation', 'High-fidelity sound', 'Multi-device pairing']
            elif cat_slug == 'camaras':
                additions = ['Weather-sealed body', 'High-speed autofocus', 'RAW shooting support']
            elif cat_slug == 'monitores':
                additions = ['Uniformity compensation', 'Hardware calibration', 'Ergonomic stand']
            elif cat_slug == 'gaming':
                additions = ['Low latency mode', 'Custom performance profiles', 'RGB lighting']

            for a in additions:
                if a not in features:
                    features.append(a)

            p.features = features
            p.save()
            updated += 1

        self.stdout.write(self.style.SUCCESS(f'Expanded specs and features for {updated} products'))
