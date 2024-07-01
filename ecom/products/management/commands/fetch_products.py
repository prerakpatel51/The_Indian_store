from django.core.management.base import BaseCommand
import requests
from products.models import Category, Product, ProductImage
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image as PILImage
import os,PIL

class Command(BaseCommand):
    help = 'Fetch products from an API and save them to the database'

    def handle(self, *args, **options):
        url = 'https://api.escuelajs.co/api/v1/products'
        response = requests.get(url)
        if response.status_code == 200:
            products_data = response.json()
            for product_data in products_data:
                try:
                    # Handle category data
                    category_data = product_data.get('category', {})
                    category, _ = Category.objects.get_or_create(
                        id=category_data.get('id'),
                        defaults={
                            'category_name': category_data.get('name'),
                            'category_image': category_data.get('image')
                        }
                    )

                    # Handle product data
                    product, _ = Product.objects.update_or_create(
                        id=product_data.get('id'),
                        defaults={
                            'product_name': product_data.get('title'),
                            'category': category,
                            'price': product_data.get('price'),
                            'product_description': product_data.get('description')
                        }
                    )

                    # Handle product images
                    for image_url in product_data.get('images', []):
                        try:
                            image_name = os.path.basename(image_url)
                            image_data = requests.get(image_url).content
                            
                            # Attempt to open image using PIL to verify it's a valid image
                            try:
                                PILImage.open(BytesIO(image_data))
                            except PIL.UnidentifiedImageError:
                                self.stdout.write(self.style.ERROR(f"Image '{image_name}' is not a valid image file"))

                            image_file = ContentFile(image_data)
                            product_image = ProductImage(
                                product=product
                            )
                            product_image.image.save(image_name, image_file, save=True)
                            self.stdout.write(self.style.SUCCESS(f"Image '{image_name}' for product '{product.product_name}' created successfully"))
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f"Failed to save image '{image_url}' for product '{product.product_name}': {e}"))
                            continue
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed to process product data: {e}"))
                    continue
        else:
            self.stdout.write(self.style.ERROR('Failed to fetch products from the API'))
