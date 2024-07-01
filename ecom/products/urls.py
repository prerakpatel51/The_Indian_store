from django.urls import path
from products.views import get_products ,add_rating

urlpatterns = [
    path('<slug>/',get_products,name='get_product'), 
      path('s/product<slug>/rate/', add_rating, name='add_rating'),
  ]