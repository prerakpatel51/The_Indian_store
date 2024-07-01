from django.shortcuts import render
from products.models import Category, Product
from django.contrib.auth.decorators import login_required


def index(request):
    categories = {
        'men_clothes_category': Category.objects.filter(category_name="men's clothing"),
        'women_clothes_category': Category.objects.filter(category_name="women's clothing"),
        'general_clothes_category': Category.objects.filter(category_name="clothes"),
        'home_appliances': Category.objects.filter(category_name="home appliances"),
        'electronics': Category.objects.filter(category_name="electronics"),
        'food': Category.objects.filter(category_name='food'),
        'Jewelry': Category.objects.filter(category_name='Jewelry'),
        'sports': Category.objects.filter(category_name='sports and outdoors'),
        'beauty': Category.objects.filter(category_name='beauty and personal care')
    }
    
    context = categories
    
    return render(request, 'home/index.html', context)
