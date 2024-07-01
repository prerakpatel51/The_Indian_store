from django.db import models
# Create your models here.
from base.models import BaseModel
from django.utils.text import slugify
from django.contrib.auth.models import User



class Category(BaseModel):
    category_name=models.CharField(max_length=100)
    slug=models.SlugField(unique=True,null=True,blank=True)
    category_image=models.ImageField(upload_to='categories',blank=True)
        
    def save(self,*args,**kwargs):
        self.slug=slugify(self.category_name)
        super(Category,self).save(*args,**kwargs)


    def __str__(self)->str:
        return self.category_name




class ColorVariant(BaseModel):
    color_name=models.CharField(max_length=100)
    price=models.IntegerField(default=0)
    
    def __str__(self)->str:
        return self.color_name
        
        
        
    
class SizeVariant(BaseModel):
    size_name=models.CharField(max_length=100)
    price=models.IntegerField(default=0)
    
    def __str__(self)->str:
        return self.size_name



class Product(BaseModel):
    product_name=models.CharField(max_length=100)
    slug=models.SlugField(unique=True,blank=True,null=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    price=models.IntegerField()
    
    product_description=models.TextField()
    color_variant=models.ManyToManyField(ColorVariant,blank=True)
    size_variant=models.ManyToManyField(SizeVariant,blank=True)
        
    def save(self,*args,**kwargs):
        self.slug=slugify(self.product_name)
        super(Product,self).save(*args,**kwargs)


    def __str__(self)->str:
        return self.product_name
    
    def get_product_price_by_size_color(self,size,color):
        print(self.price +SizeVariant.objects.get(size_name=size).price +ColorVariant.objects.get(color_name=color).price)
        return (self.price +SizeVariant.objects.get(size_name=size).price +ColorVariant.objects.get(color_name=color).price)
    
    
    # def get_average_rating(self):
    #     ratings = self.ratings.all()
    #     if ratings:
    #         return sum([rating.rating for rating in ratings]) / len(ratings)
    #     return 0




class ProductImage(BaseModel):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_images")
    image=models.ImageField(upload_to="product")
    
    
    
    
class Coupon(BaseModel):
    coupon_code=models.CharField(max_length=100)
    is_expired=models.BooleanField(default=False)
    discount_price=models.IntegerField(default=100)
    minimum_amount=models.IntegerField(default=500)
    
    
    

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')

    def __str__(self):
        return f'{self.product.product_name} - {self.rating} stars'