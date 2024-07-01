import os
import requests
from django.core.files import File
from django.utils.text import slugify
from products.models import Category, Product, ProductImage

# Replace with your Unsplash Access Key
UNSPLASH_ACCESS_KEY = 'sHu3GZybbROCiytJd4Nyxdmtd8I3GIoTd5HRuaGuAEk'
products = [
    {"name": "Yoga Mat", "category": "sports and outdoors", "description": "High-density yoga mat for better practice.", "price": 70},
    {"name": "Barbell Dumbbells", "category": "sports and outdoors", "description": "Durable dumbbells for strength training.", "price": 30},
    {"name": "Resistance Bands", "category": "sports and outdoors", "description": "Set of resistance bands for workouts.", "price": 15},
    {"name": "Mountain Bike", "category": "sports and outdoors", "description": "Durable mountain bike for all terrains.", "price": 400},
    {"name": "Camping Tent", "category": "sports and outdoors", "description": "Spacious and weather-resistant camping tent.", "price": 120},
    {"name": "Sports Sleeping Bag", "category": "sports and outdoors", "description": "Warm and comfortable sleeping bag.", "price": 60},
    {"name": "Under Armour Sportswear", "category": "sports and outdoors", "description": "High-performance sportswear.", "price": 40},
    {"name": "Hiking Boots", "category": "sports and outdoors", "description": "Durable and comfortable hiking boots.", "price": 100},
    {"name": "Water Bottle", "category": "sports and outdoors", "description": "Insulated water bottle to keep drinks cold.", "price": 30},
    {"name": "Fitbit Fitness Tracker", "category": "sports and outdoors", "description": "Advanced fitness tracker for monitoring activities.", "price": 150},
]


def fetch_image(product_name):
    query = product_name.replace(" ", "+")
    url = f"https://api.unsplash.com/search/photos?query={query}&client_id={UNSPLASH_ACCESS_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            return data['results'][0]['urls']['small']
    return None

def save_image_from_url(url, product_name):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        file_name = f"{slugify(product_name)}.jpg"
        with open(file_name, 'wb') as out_file:
            out_file.write(response.content)
        return file_name
    return None

def store_product(product_data):
    category, created = Category.objects.get_or_create(category_name=product_data["category"])
    product = Product(
        product_name=product_data["name"],
        category=category,
        product_description=product_data["description"],
        price=product_data["price"],
    )
    product.save()
    
    image_url = fetch_image(product_data["name"])
    if image_url:
        image_path = save_image_from_url(image_url, product_data["name"])
        if image_path:
            with open(image_path, 'rb') as image_file:
                product_image = ProductImage(product=product, image=File(image_file))
                product_image.save()
            os.remove(image_path)

if __name__ == "__main__":
    for product_data in products:
        store_product(product_data)
    print('Successfully loaded products')
