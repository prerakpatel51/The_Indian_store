from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .models import Product,SizeVariant,ColorVariant
from .models import  Rating
from .forms import RatingForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
@login_required
def get_products(request,slug):
    try:
       
        product=Product.objects.get(slug=slug)
        
        ratings = product.ratings.all()
        rating_form = RatingForm()
        context={'product':product}
        context['ratings']=ratings
        context['rating_form']=rating_form
        if request.GET.get('size') and request.GET.get('color'):
            size=request.GET.get('size')
            color=request.GET.get('color')
           
            price=product.get_product_price_by_size_color(size,color)
            
            context['selected_size']=size
            context['selected_color']=color
           
            
            context['updated_price']=price
            print(size)
            print(color)
            print(price)
        return render(request,'product/product.html',context)
    except Exception as e:
        print(e)
 
 
 

@login_required
def add_rating(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.product = product
            rating.user = request.user
            try:
                rating.save()
                messages.success(request, 'Rating submitted successfully.')
            except:
                messages.error(request, 'You have already rated this product.')
        else:
            messages.error(request, 'There was an error submitting your rating.')
    return redirect('get_product', slug=product.slug)
 
 
 
 
 