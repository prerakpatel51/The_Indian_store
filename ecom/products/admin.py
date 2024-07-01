# from django.contrib import admin
# from .models import *

# admin.site.register(Category)

# class ProductImageAdmin(admin.StackedInline):
#     model=ProductImage
    
# class ProductAdmin(admin.ModelAdmin):
#     list_display=['product_name','price']
#     inlines=[ProductImageAdmin]
    
# @admin.register(ColorVariant)    
# class ColorVariantAdmin(admin.ModelAdmin):
#     model=ColorVariant
#     list_display=['color_name','price']
    
    
    
# @admin.register(SizeVariant)
# class SizeVariantAdmin(admin.ModelAdmin):
#     model=SizeVariant
#     list_display=['size_name','price']
    

# admin.site.register(Product,ProductAdmin) 

# admin.site.register(Coupon)


from django.contrib import admin
from .models import *

admin.site.register(Category)

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'category', 'price']
    search_fields = ['product_name', 'product_description']
    list_filter = ['category']
    inlines = [ProductImageAdmin]
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(ColorVariant)    
class ColorVariantAdmin(admin.ModelAdmin):
    list_display = ['color_name', 'price']

@admin.register(SizeVariant)
class SizeVariantAdmin(admin.ModelAdmin):
    list_display = ['size_name', 'price']

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['coupon_code', 'is_expired', 'discount_price', 'minimum_amount']




admin.site.register(ProductImage)