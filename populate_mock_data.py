import os
import shutil
import django

# Set up django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotwheels_project.settings.local')
django.setup()

from products.models import Category, Product, ProductImage

# Paths
media_products_dir = os.path.abspath('media/products')
os.makedirs(media_products_dir, exist_ok=True)

# Sources
sources = {
    'twin_mill': r'C:\Users\Athul\.gemini\antigravity-ide\brain\fea2f2cb-8fc4-4e45-bf05-617d7353b715\twin_mill_1780585148082.png',
    'bone_shaker': r'C:\Users\Athul\.gemini\antigravity-ide\brain\fea2f2cb-8fc4-4e45-bf05-617d7353b715\bone_shaker_1780585167399.png',
    'deora_ii': r'C:\Users\Athul\.gemini\antigravity-ide\brain\fea2f2cb-8fc4-4e45-bf05-617d7353b715\deora_ii_1780585183824.png',
}

# Copy files
for name, src in sources.items():
    dest = os.path.join(media_products_dir, f"{name}.png")
    print(f"Copying {src} to {dest}")
    try:
        shutil.copy(src, dest)
    except Exception as e:
        print(f"Error copying {src}: {e}")

# Create categories
street_racers, _ = Category.objects.get_or_create(
    slug='street-racers',
    defaults={'name': 'Street Racers', 'description': 'Bold street-legal performance cars built for collectors.'}
)

collector_editions, _ = Category.objects.get_or_create(
    slug='collector-editions',
    defaults={'name': 'Collector Editions', 'description': 'Limited release cars with premium paint, packaging, and detail.'}
)

# Create/Update Products
products_data = [
    {
        'category': street_racers,
        'title': 'Twin Mill Classic',
        'slug': 'twin-mill-classic',
        'summary': 'The iconic dual-engine classic muscle racer.',
        'description': 'A legendary Hot Wheels design featuring dual supercharged engines chrome-plated on the front hood and a candy apple red paint job.',
        'price': 29.99,
        'stock': 15,
        'is_active': True,
        'featured': True,
        'image_filename': 'twin_mill.png'
    },
    {
        'category': collector_editions,
        'title': 'Bone Shaker Hot Rod',
        'slug': 'bone-shaker-hot-rod',
        'summary': 'The ultimate bad-to-the-bone hot rod racer.',
        'description': 'One of the most famous Hot Wheels designs of all time, featuring a chrome skull grille, open engine bay, and matte black finish with flame decals.',
        'price': 34.99,
        'stock': 8,
        'is_active': True,
        'featured': True,
        'image_filename': 'bone_shaker.png'
    },
    {
        'category': street_racers,
        'title': 'Deora II Surf Wagon',
        'slug': 'deora-ii-surf-wagon',
        'summary': 'Futuristic aerodynamic cruiser carrying surfboards.',
        'description': 'A beloved casting with a unique curved bubble-canopy cabin design, sleek metallic blue body, and custom surfboards mounted on the back.',
        'price': 27.99,
        'stock': 12,
        'is_active': True,
        'featured': True,
        'image_filename': 'deora_ii.png'
    }
]

for p_data in products_data:
    filename = p_data.pop('image_filename')
    product, created = Product.objects.update_or_create(
        slug=p_data['slug'],
        defaults=p_data
    )
    # Clear existing images to avoid duplicates, then add
    ProductImage.objects.filter(product=product).delete()
    ProductImage.objects.create(
        product=product,
        image=f"products/{filename}",
        alt_text=product.title,
        is_main=True
    )
    print(f"Set product {product.title} with image products/{filename}")

print("Database population completed successfully!")
