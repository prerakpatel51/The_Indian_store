import os
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from products.models import Category, Product, ProductImage
from django.utils.text import slugify
# Create media directory if it doesn't exist
media_dir = 'media/sample_images'
if not os.path.exists(media_dir):
    os.makedirs(media_dir)

# Fetch product data from API
response = requests.get('https://fakestoreapi.com/products')
products_data = response.json()

# Helper function to download and save images
def download_image(url, product_name):
    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(requests.get(url).content)
    img_temp.flush()
    return File(img_temp, name=f"{slugify(product_name)}.jpg")

# Create or get category
def get_or_create_category(category_name):
    category, created = Category.objects.get_or_create(
        category_name=category_name,
        defaults={'slug': slugify(category_name)}
    )
    return category

# Create products
for product_data in products_data:
    category = get_or_create_category(product_data['category'])
    
    # Create product instance
    product = Product.objects.create(
        product_name=product_data['title'],
        category=category,
        price=product_data['price'],
        product_description=product_data['description']
    )
    
    # Download and save product image
    image_file = download_image(product_data['image'], product.product_name)
    product_image = ProductImage.objects.create(
        product=product,
        image=image_file
    )

    print(f"Created product: {product.product_name}")

print(f"Created {len(products_data)} products.")