from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.utils import timezone
import random

from products.models import Category, Product


REAL_PRODUCTS = {
    'smartphones': [
        {
            'name': 'Apple iPhone 14 Pro',
            'brand': 'Apple',
            'model': 'iPhone 14 Pro',
            'short_description': 'Smartphone premium con cámara avanzada y pantalla ProMotion.',
            'description': 'iPhone 14 Pro con A16 Bionic, sistema de cámaras Pro, pantalla Super Retina XDR con ProMotion, y iOS. Ideal para fotografía y rendimiento.',
            'specifications': {
                'CPU': 'A16 Bionic',
                'Display': '6.1" Super Retina XDR ProMotion',
                'Storage': '128/256/512/1TB',
                'RAM': '6 GB (estimado)',
                'Battery': '~3200 mAh (optimizado)',
                'OS': 'iOS',
            },
            'features': ['Cámara Pro de 48MP', 'Pantalla ProMotion 120Hz', 'Face ID', 'Carga MagSafe']
        },
        {
            'name': 'Samsung Galaxy S23 Ultra',
            'brand': 'Samsung',
            'model': 'Galaxy S23 Ultra',
            'short_description': 'Smartphone Android de gama alta con zoom óptico y gran batería.',
            'description': 'Samsung Galaxy S23 Ultra con pantalla AMOLED de alta tasa de refresco, potente cámara con zoom óptico y rendimiento para multitarea y gaming.',
            'specifications': {
                'CPU': 'Snapdragon 8 Gen 2 / Exynos (región)',
                'Display': '6.8" Dynamic AMOLED',
                'Storage': '256/512/1TB',
                'RAM': '8/12 GB',
                'Battery': '5000 mAh',
                'OS': 'Android',
            },
            'features': ['Zoom óptico 10x', 'S Pen (según modelo)', 'Carga rápida', 'Pantalla HDR']
        },
        {
            'name': 'Google Pixel 7 Pro',
            'brand': 'Google',
            'model': 'Pixel 7 Pro',
            'short_description': 'Experiencia Android pura con cámara computacional avanzada.',
            'description': 'Pixel 7 Pro con Tensor G2, cámara con procesamiento de imagen avanzado, actualizaciones directas de Google y funciones AI integradas.',
            'specifications': {
                'CPU': 'Google Tensor G2',
                'Display': '6.7" AMOLED',
                'Storage': '128/256/512 GB',
                'RAM': '12 GB',
                'Battery': '5000 mAh',
                'OS': 'Android',
            },
            'features': ['Cámara computacional', 'Actualizaciones garantizadas', 'Asistente mejorado']
        },
        {
            'name': 'OnePlus 11',
            'brand': 'OnePlus',
            'model': '11',
            'short_description': 'Teléfono rápido y optimizado para rendimiento y carga veloz.',
            'description': 'OnePlus 11 con chipset de alta gama, carga rápida y una experiencia OxygenOS fluida.',
            'specifications': {
                'CPU': 'Snapdragon 8 Gen 2',
                'Display': '6.7" AMOLED 120Hz',
                'Storage': '128/256/512 GB',
                'RAM': '8/16 GB',
                'Battery': '5000 mAh',
                'OS': 'Android (OxygenOS)'
            },
            'features': ['Carga super rápida', 'Rendimiento gaming', 'OxygenOS fluido']
        },
        {
            'name': 'Xiaomi 13 Pro',
            'brand': 'Xiaomi',
            'model': '13 Pro',
            'short_description': 'Alta relación calidad/precio con cámara Leica y carga rápida.',
            'description': 'Xiaomi 13 Pro con cámara co-desarrollada por Leica, pantalla de gran calidad y componentes de alto rendimiento.',
            'specifications': {'CPU': 'Snapdragon 8 Gen 2', 'Display': '6.73" AMOLED', 'RAM': '8/12 GB', 'Storage': '128/256/512 GB', 'Battery': '4820 mAh', 'OS': 'Android'},
            'features': ['Cámara Leica', 'Carga rápida', 'Pantalla HDR']
        }
    ],

    'laptops': [
        {'name': 'Apple MacBook Air (M2)', 'brand': 'Apple', 'model': 'MacBook Air M2', 'short_description': 'Ultraligero con chip Apple M2 y gran autonomía.',
         'description': 'MacBook Air con Apple M2, excelente eficiencia energética y rendimiento para productividad y multimedia.',
         'specifications': {'CPU': 'Apple M2', 'RAM': '8/16 GB', 'Storage': '256/512 GB', 'Display': '13.6" Retina', 'Battery': 'Hasta 18h'},
         'features': ['Diseño delgado', 'Silent fanless', 'Integración Apple']},
        {'name': 'Dell XPS 13', 'brand': 'Dell', 'model': 'XPS 13', 'short_description': 'Portátil compacto y potente para profesionales.',
         'description': 'Dell XPS 13 con chasis premium, pantalla InfinityEdge y opciones de hardware de última generación.',
         'specifications': {'CPU': 'Intel Core i5/i7', 'RAM': '8/16 GB', 'Storage': '256/512/1TB', 'Display': '13.4" FHD/4K'},
         'features': ['Chasis premium', 'Pantalla nítida', 'Buen rendimiento']},
        {'name': 'HP Spectre x360', 'brand': 'HP', 'model': 'Spectre x360', 'short_description': 'Convertible 2-en-1 con buena autonomía.',
         'description': 'HP Spectre x360 convertible con bisagra 360°, táctil y opciones OLED.',
         'specifications': {'CPU': 'Intel Core i5/i7', 'RAM': '8/16 GB', 'Storage': '256/512 GB', 'Display': '13-14" OLED opcional'},
         'features': ['Convertible', 'Pantalla táctil', 'Diseño atractivo']},
        {'name': 'Lenovo ThinkPad X1 Carbon', 'brand': 'Lenovo', 'model': 'X1 Carbon', 'short_description': 'Ligero, resistente y orientado a empresas.',
         'description': 'ThinkPad X1 Carbon con teclado excelente, robustez y opciones empresariales de seguridad.',
         'specifications': {'CPU': 'Intel Core i5/i7', 'RAM': '8-32 GB', 'Storage': '256-1TB', 'Display': '14"'},
         'features': ['Teclado cómodo', 'Seguridad empresarial', 'Ligero']},
        {'name': 'Asus ROG Zephyrus', 'brand': 'ASUS', 'model': 'ROG Zephyrus', 'short_description': 'Gaming portátil con GPU dedicada.',
         'description': 'Asus ROG Zephyrus pensado para gaming con GPU potentes, refrigeración avanzada y pantalla de alta tasa de refresco.',
         'specifications': {'CPU': 'AMD/Intel high-end', 'GPU': 'NVIDIA RTX series', 'RAM': '16/32 GB', 'Storage': '512 GB+','Display':'15-17" 144-240Hz'},
         'features': ['GPU dedicada', 'Alta tasa de refresco', 'Refrigeración avanzada']}
    ],

    'tablets': [
        {'name': 'Apple iPad Air', 'brand': 'Apple', 'model': 'iPad Air', 'short_description': 'Tablet ligera con rendimiento excelente.',
         'description': 'iPad Air con chip rápido, excelente pantalla y amplia compatibilidad con accesorios.',
         'specifications': {'CPU':'Apple M1/M2', 'Display':'10.9" Liquid Retina', 'Storage':'64/256 GB', 'Battery':'Hasta 10h'}, 'features':['Compatibilidad Apple Pencil','Ligera']},
        {'name': 'Samsung Galaxy Tab S8', 'brand': 'Samsung', 'model': 'Galaxy Tab S8', 'short_description':'Tablet Android de alta gama', 'description':'Galaxy Tab S8 con S Pen y pantalla de alta calidad.', 'specifications':{'CPU':'Snapdragon 8','Display':'11" LTPS','RAM':'8 GB','Storage':'128 GB'}, 'features':['S Pen incluido','Multitarea']},
        {'name': 'Lenovo Tab P11', 'brand': 'Lenovo', 'model': 'Tab P11', 'short_description':'Tablet equilibrada para multimedia', 'description':'Tablet con buena pantalla para consumo de contenido.', 'specifications':{'CPU':'MediaTek','Display':'11"','RAM':'4-6 GB','Storage':'64-128 GB'}, 'features':['Buena relación calidad/precio']},
        {'name': 'Amazon Fire HD 10', 'brand': 'Amazon', 'model': 'Fire HD 10', 'short_description':'Tablet económica enfocada en contenido', 'description':'Fire HD 10 para consumo de contenido Amazon con buena autonomía.', 'specifications':{'CPU':'MediaTek','Display':'10.1"','Storage':'32/64 GB'}, 'features':['Económica','Buen consumo multimedia']},
        {'name': 'Microsoft Surface Go', 'brand': 'Microsoft', 'model': 'Surface Go', 'short_description':'Tablet Windows compacta', 'description':'Surface Go ligera con Windows para productividad básica.', 'specifications':{'CPU':'Intel','Display':'10"','RAM':'4-8 GB'}, 'features':['Windows real','Portátil']}
    ],

    'accesorios': [
        {'name':'Apple AirPods Pro','brand':'Apple','model':'AirPods Pro','short_description':'Auriculares in-ear con cancelación activa de ruido','description':'AirPods Pro con ANC, modo transparencia y buen emparejamiento con dispositivos Apple.','specifications':{'Connectivity':'Bluetooth','Battery':'~24h con estuche'},'features':['ANC','Resistente al agua IPX4']},
        {'name':'Logitech MX Master 3','brand':'Logitech','model':'MX Master 3','short_description':'Ratón inalámbrico para productividad','description':'Ratón ergonómico con rueda MagSpeed, personalizable y con larga autonomía.','specifications':{'Connectivity':'Bluetooth/USB','Battery':'70 días'},'features':['Ergonómico','Preciso','Botones programables']},
        {'name':'Anker PowerCore 20100','brand':'Anker','model':'PowerCore 20100','short_description':'Batería portátil de alta capacidad','description':'Power bank para múltiples cargas con salida USB-A y USB-C opcional.','specifications':{'Capacity':'20100 mAh'},'features':['Alta capacidad','Carga rápida']},
        {'name':'SanDisk Extreme 128GB','brand':'SanDisk','model':'Extreme 128GB','short_description':'Tarjeta microSD de alto rendimiento','description':'microSD para fotos y video 4K con velocidades altas de lectura/escritura.','specifications':{'Capacity':'128 GB','Speed':'A2/U3'},'features':['4K Ready','Alta velocidad']},
        {'name':'Belkin USB-C Hub 7-en-1','brand':'Belkin','model':'USB-C Hub','short_description':'Hub multiporta para laptops','description':'Hub con HDMI, Ethernet, USB-A y lector SD para expandir puertos.', 'specifications':{'Ports':'HDMI, Ethernet, USB, SD'},'features':['Multipuerto','Plug-and-play']}
    ],

    'audio': [
        {'name':'Sony WH-1000XM5','brand':'Sony','model':'WH-1000XM5','short_description':'Auriculares con cancelación líder del mercado','description':'Auriculares over-ear con ANC avanzada, gran autonomía y calidad de sonido.', 'specifications':{'Battery':'~30h','Connectivity':'Bluetooth 5.2'}, 'features':['ANC avanzado','Sonido equilibrado']},
        {'name':'Bose QuietComfort 45','brand':'Bose','model':'QC45','short_description':'Auriculares cómodos con excelente cancelación', 'description':'QC45 con confort y sonido claro para largas sesiones.', 'specifications':{'Battery':'~24h'}, 'features':['Muy cómodos','Buen ANC']},
        {'name':'Sennheiser HD 600','brand':'Sennheiser','model':'HD 600','short_description':'Auriculares abiertos para audiófilos', 'description':'HD 600 con perfil sonoro neutro ideal para escuchas críticas.', 'specifications':{'Type':'Open-back'}, 'features':['Sonido natural']},
        {'name':'JBL Charge 5','brand':'JBL','model':'Charge 5','short_description':'Altavoz portátil resistente', 'description':'Bluetooth speaker con buena batería y sonido potente.', 'specifications':{'Battery':'~20h'}, 'features':['Portátil','Resistente al agua']},
        {'name':'Marshall Major IV','brand':'Marshall','model':'Major IV','short_description':'Auriculares con estilo retro y buena autonomía','description':'Auriculares on-ear con estética clásica y sonido cálido.', 'specifications':{'Battery':'~80h'}, 'features':['Estética retro','Larga batería']}
    ],

    'camaras': [
        {'name':'Canon EOS R6','brand':'Canon','model':'EOS R6','short_description':'Cámara mirrorless versátil para foto y video','description':'Canon R6 con excelente rendimiento en baja luz y estabilización incorporada.', 'specifications':{'Sensor':'Full-frame','Megapixels':'20 MP'}, 'features':['IBIS','Excelente AF']},
        {'name':'Sony Alpha a7 III','brand':'Sony','model':'a7 III','short_description':'Cámara full-frame equilibrada','description':'Sony a7 III con gran rendimiento ISO y buen conjunto para fotógrafos.', 'specifications':{'Sensor':'Full-frame','Megapixels':'24 MP'}, 'features':['Buen ISO','Autofocus rápido']},
        {'name':'Nikon Z6 II','brand':'Nikon','model':'Z6 II','short_description':'Mirrorless full-frame para profesionales', 'description':'Z6 II con buen rendimiento en vídeo y foto.', 'specifications':{'Sensor':'Full-frame','Megapixels':'24 MP'}, 'features':['Dual card slots','Video-capable']},
        {'name':'Fujifilm X-T4','brand':'Fujifilm','model':'X-T4','short_description':'Cámara APS-C con gran colorimetría','description':'X-T4 con estabilización y color típico Fujifilm.', 'specifications':{'Sensor':'APS-C','Megapixels':'26 MP'}, 'features':['Color Fujifilm','IBIS']},
        {'name':'Panasonic Lumix GH5','brand':'Panasonic','model':'GH5','short_description':'Cámara orientada a video profesional','description':'GH5 con capacidades de video avanzadas y cuerpo robusto.', 'specifications':{'Sensor':'Micro Four Thirds','Video':'4K 60p'}, 'features':['Video profesional','Build quality']}
    ],

    'monitores': [
        {'name':'Dell UltraSharp U2720Q','brand':'Dell','model':'U2720Q','short_description':'Monitor 4K para profesionales', 'description':'Monitor 27" 4K con alta fidelidad de color y puertos USB-C.', 'specifications':{'Size':'27"','Resolution':'3840x2160'}, 'features':['4K','Color preciso']},
        {'name':'LG 27GN950','brand':'LG','model':'27GN950','short_description':'Gaming 4K 144Hz', 'description':'Monitor gaming 4K con alta tasa de refresco y baja latencia.', 'specifications':{'Size':'27"','Resolution':'4K','Refresh':'144Hz'}, 'features':['4K 144Hz','G-Sync compatible']},
        {'name':'ASUS ProArt PA32UCX','brand':'ASUS','model':'PA32UCX','short_description':'Monitor profesional HDR', 'description':'Monitor para edición de color profesional con HDR y amplio gamut.', 'specifications':{'Size':'32"','Resolution':'4K'}, 'features':['HDR','Alta precisión de color']},
        {'name':'Samsung Odyssey G7','brand':'Samsung','model':'Odyssey G7','short_description':'Monitor curvo gaming', 'description':'Curved monitor con altas tasas de refresco y buen contraste VA.', 'specifications':{'Size':'27-32"','Refresh':'240Hz'}, 'features':['Curvo','Alta tasa de refresco']},
        {'name':'BenQ PD2700U','brand':'BenQ','model':'PD2700U','short_description':'Monitor 4K orientado a diseñadores', 'description':'Monitor con modos de color y ergonomía para profesionales creativos.', 'specifications':{'Size':'27"','Resolution':'4K'}, 'features':['Modos de color','Ergonomía']}
    ],

    'gaming': [
        {'name':'PlayStation 5','brand':'Sony','model':'PS5','short_description':'Consola de última generación', 'description':'PS5 con GPU y CPU custom de alta potencia, soporte 4K y catálogo exclusivo de juegos.', 'specifications':{'Type':'Consola','Storage':'825 GB SSD'}, 'features':['Load times rápidos','Juegos exclusivos']},
        {'name':'Xbox Series X','brand':'Microsoft','model':'Series X','short_description':'Consola potente para gaming', 'description':'Xbox Series X con hardware potente y compatibilidad con títulos anteriores.', 'specifications':{'Type':'Consola','Storage':'1 TB SSD'}, 'features':['Backward compatibility','Potencia bruta']},
        {'name':'Nintendo Switch OLED','brand':'Nintendo','model':'Switch OLED','short_description':'Consola híbrida portátil y de sobremesa', 'description':'Switch OLED con pantalla mejorada y gran catálogo familiar.', 'specifications':{'Type':'Híbrida','Storage':'64 GB'}, 'features':['Modo portátil','Juegos exclusivos']},
        {'name':'Razer Blade 15','brand':'Razer','model':'Blade 15','short_description':'Portátil gaming premium', 'description':'Razer Blade con GPU dedicada y diseño delgado.', 'specifications':{'CPU':'Intel','GPU':'NVIDIA RTX'}, 'features':['GPU potente','Construcción premium']},
        {'name':'MSI GF65','brand':'MSI','model':'GF65','short_description':'Gaming accesible', 'description':'MSI GF65 como opción gaming con buena relación calidad/precio.', 'specifications':{'CPU':'Intel','GPU':'NVIDIA GTX/RTX'}, 'features':['Buena relación calidad/precio']}
    ]
}


class Command(BaseCommand):
    help = 'Enrich demo products: replace generic demo product names with real product names and fill descriptions/specs/features (no images)'

    def handle(self, *args, **options):
        self.stdout.write('Starting enrichment of demo products...')

        categories = Category.objects.all()
        updated = 0
        for cat in categories:
            key = slugify(cat.name).lower()
            if key not in REAL_PRODUCTS:
                continue

            templates = REAL_PRODUCTS[key]
            # Find products created for this category that look like demo entries
            qs = Product.objects.filter(category=cat).order_by('id')
            # Prefer products whose name starts with the category (created by demo script)
            demo_products = [p for p in qs if p.name.lower().startswith(cat.name.lower())]
            if not demo_products:
                # fallback: use all products in the category
                demo_products = list(qs)

            for i, prod in enumerate(demo_products):
                template = templates[i % len(templates)]
                old_name = prod.name
                prod.name = template['name']
                # keep existing slug to avoid breaking links
                prod.brand = template.get('brand', prod.brand)
                prod.model = template.get('model', prod.model)
                prod.short_description = template.get('short_description', prod.short_description)
                prod.description = template.get('description', prod.description)
                # merge specifications and move any template features into specifications under 'Características'
                specs = dict(prod.specifications or {})
                specs.update(template.get('specifications', {}))
                tpl_features = template.get('features', []) or []
                if tpl_features:
                    existing_feats = specs.get('Características', [])
                    if not isinstance(existing_feats, list):
                        existing_feats = [existing_feats]
                    for f in tpl_features:
                        if f not in existing_feats:
                            existing_feats.append(f)
                    specs['Características'] = existing_feats
                prod.specifications = specs
                # update SKU if missing
                if not prod.sku:
                    prod.sku = f"SKU-{random.randint(100000,999999)}"
                # adjust price slightly if not already set
                try:
                    price_ok = float(prod.price) > 0
                except Exception:
                    price_ok = False
                if not price_ok:
                    prod.price = round(random.uniform(49.99, 1999.99), 2)
                prod.published_at = timezone.now()
                prod.save()
                updated += 1
                self.stdout.write(f'Updated product: "{old_name}" -> "{prod.name}"')

        self.stdout.write(self.style.SUCCESS(f'Enrichment complete. Updated {updated} products.'))
