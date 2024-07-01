import os
import random
import requests
from io import BytesIO
from django.core.files import File
from django.core.management.base import BaseCommand
from faker import Faker
from products.models import Category, ColorVariant, SizeVariant, Product, ProductImage

# Replace with your Unsplash Access Key and Secret Key
UNSPLASH_ACCESS_KEY = '4xEiK-mSp9fQnIU2NhGN7J50F44WxT6QKwyjrz7hGAM'
UNSPLASH_SECRET_KEY = 'AmMkjKCzjcud-1kn7FAssqbDiMxyRk6O4DniSzeBq68'

class Command(BaseCommand):
    help = 'Populate the database with random products'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create categories if not exists
        categories = ['Home Decor', 'Clothes', 'Electronics', 'Books', 'Toys', 'Kitchen', 'Sports', 'Beauty', 'Tools', 'Pets']
        for category_name in categories:
            Category.objects.get_or_create(category_name=category_name)

        # Define some color and size variants
        colors = ['Red', 'Blue', 'Green', 'Yellow', 'Black']
        sizes = ['S', 'M', 'L', 'XL','XS','XXL']

        num_products = 50
        for i in range(num_products):
            product_name = f"Product {i+1}"
            price = random.randint(100, 1000)
            category = Category.objects.get(category_name=random.choice(categories))

            # Fetch a random image and description from Unsplash
            response = requests.get(
                f"https://api.unsplash.com/photos/random?query=product&client_id={UNSPLASH_ACCESS_KEY}"
            )
            if response.status_code == 200:
                data = response.json()
                product_description = data['alt_description'] or fake.text()
                image_url = data['urls']['small']
                response = requests.get(image_url)
                image = BytesIO(response.content)
                image_name = f"product_{i+1}.jpg"
                image_path = os.path.join('media/sample_images', image_name)

                # Save the image locally
                with open(image_path, 'wb') as f:
                    f.write(image.getbuffer())

                # Create the product
                product = Product.objects.create(
                    product_name=product_name,
                    category=category,
                    price=price,
                    product_description=product_description
                )

                # Add color and size variants to the product
                color_variants = ColorVariant.objects.bulk_create([
                    ColorVariant(color_name=color, price=random.randint(1, 20)) for color in colors
                ])
                product.color_variant.set(random.sample(color_variants, random.randint(1, len(color_variants))))

                size_variants = SizeVariant.objects.bulk_create([
                    SizeVariant(size_name=size, price=random.randint(1, 20)) for size in sizes
                ])
                product.size_variant.set(random.sample(size_variants, random.randint(1, len(size_variants))))

                # Associate the image with the product
                with open(image_path, 'rb') as image_file:
                    product_image = ProductImage.objects.create(
                        product=product
                    )
                    product_image.image.save(image_name, File(image_file), save=True)

            else:
                self.stdout.write(self.style.ERROR(f"Failed to fetch data from Unsplash: {response.status_code}"))

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with 50 products'))
