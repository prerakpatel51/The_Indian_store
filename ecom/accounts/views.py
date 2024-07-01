from django.shortcuts import render,HttpResponseRedirect,redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Profile,Cart,CartItems
from products.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import stripe
from django.views import View
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .forms import ProfileForm
stripe.api_key = settings.STRIPE_SECRET_KEY



def login_page(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user_obj=User.objects.filter(username=email) 

        if  not user_obj.exists():
            messages.warning(request,'Account not found.')
            return HttpResponseRedirect(request.path_info)
        if not user_obj[0].profile.is_email_verified:
            messages.warning(request,'Your account is not verified')
            return HttpResponseRedirect(request.path_info)

        user_obj=authenticate(username=email,password=password)

        if user_obj:
            login(request,user_obj)
            return redirect('/')


        messages.warning(request,'Invalid Credentials')
        return HttpResponseRedirect(request.path_info)

    return render(request,'accounts/login.html')







def register_page(request):
    if request.method=='POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        user_obj=User.objects.filter(username=email) 

        if user_obj.exists():
            messages.warning(request,'Email is already taken.')
            return HttpResponseRedirect(request.path_info)

        try:
            # Validate the password
            validate_password(password)
        except ValidationError as e:
            messages.error(request, '\n'.join(e.messages))
            return HttpResponseRedirect(request.path_info)


        user_obj=User.objects.create(first_name=first_name,last_name=last_name,email=email,username=email)
        user_obj.set_password(password)
        user_obj.save()

        messages.success(request,'An email has been sent to your mail ')
        return HttpResponseRedirect(request.path_info)
    return render(request,'accounts/register.html')



@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Assuming you have a URL named 'login' for the login page






def activate_email(request , email_token):
    try:
        user = Profile.objects.get(email_token= email_token)
        user.is_email_verified = True
        user.save()
        return redirect('login')
    except Exception as e:
        return HttpResponse('Invalid Email token')









@login_required       
def add_to_cart(request,uid):
    size=request.GET.get('size')
    color=request.GET.get('color')
    product=Product.objects.get(uid=uid)
    user=request.user
    cart,_=Cart.objects.get_or_create(user=user,is_paid=False)
    cart_item=CartItems.objects.create(cart=cart,product=product,)
    if size:
        size=request.GET.get('size')
        size_variant=SizeVariant.objects.get(size_name=size)

        cart_item.size_variant=size_variant
        cart_item.save()
    if color:
        color=request.GET.get('color')
        color_variant=ColorVariant.objects.get(color_name=color)

        cart_item.color_variant=color_variant
        cart_item.save()



    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def password_change_done(request):
    return render(request,'registration/password_change_done.html')





@login_required
def remove_cart(request,cart_item_uid):
    try:
        cart_item=CartItems.objects.get(uid=cart_item_uid)
        cart_item.delete()
    except Exception as  e:
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))











@login_required
def cart(request):
    try:
        cart_obj = Cart.objects.get(is_paid=False, user=request.user)
    except Cart.DoesNotExist:
        cart_obj = None
    if request.method=='POST':
        coupon=request.POST.get('coupon')
        coupon_obj=Coupon.objects.filter(coupon_code__icontains=coupon)

        if not coupon_obj.exists():
            messages.warning(request,'Invalid Coupon')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

        if cart_obj.coupon:
            messages.warning(request,'Coupon already exists.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

        if cart_obj.get_cart_total()<coupon_obj[0].minimum_amount:
           messages.warning(request,f'Amount should be greater than {coupon_obj[0].minimum_amount}.')
           return HttpResponseRedirect(request.META.get('HTTP_REFERER','/')) 

        if coupon_obj[0].is_expired:
            messages.warning(request,'Coupon Expired.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

        cart_obj.coupon =coupon_obj[0]
        cart_obj.save()
        messages.success(request,'Coupon applied!!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))    

    context={'cart':cart_obj}
    return render(request, 'accounts/cart.html', context)




@login_required
def remove_coupon(request,cart_id):
    cart=Cart.objects.get(uid=cart_id)
    cart.coupon=None
    cart.save()

    messages.success(request,'Coupon removed!!')


    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))    




@login_required
def success_view(request):
    messages.success(request, 'Your order has been placed successfully and will be delivered to you shortly')
    messages.success(request, 'Your order summary has been sent to you via email')

    session_id = request.GET.get('session_id')

    if session_id:
        checkout_session = stripe.checkout.Session.retrieve(session_id)
        if checkout_session.payment_status == 'paid':
            # Mark the cart as paid
            user = request.user
            carts = Cart.objects.filter(user=user, is_paid=False)

            for cart in carts:
                cart.is_paid = True
                cart.save()

            # Prepare email content with purchased items table
            subject = 'Order Confirmation'
            recipient_list = [user.email]

            # Get paid carts for the user
            paid_carts = Cart.objects.filter(user=request.user, is_paid=True)

            # Prepare data for the email template
            context = {
                'user': user,
                'paid_carts': paid_carts,
            }

            # Render the email template to string
            email_message = render_to_string('accounts/email_order_confirmation.html', context)

            # Send email
            send_mail(
                subject,
                email_message,
                settings.EMAIL_HOST_USER,
                recipient_list,
                html_message=email_message,  # Enable HTML content in the email
                fail_silently=False,
            )

    # Fetch all paid orders for the user to display in success.html
    paid_carts = Cart.objects.filter(user=request.user, is_paid=True)

    return render(request, 'accounts/success.html', {'paid_carts': paid_carts})



@login_required
def cancel_view(request):
    return render(request, 'accounts/cancel.html')






@login_required
def track_status(request):
    # Retrieve all purchased items for the user
    user = request.user
    purchased_items = CartItems.objects.filter(cart__user=user, cart__is_paid=True)

    return render(request, 'accounts/track_status.html', {'purchased_items': purchased_items})




class CreateCheckoutSessionView(View):

    def post(self, request):
        user = request.user
        carts = Cart.objects.filter(user=user, is_paid=False)


        if not carts:
            return JsonResponse({'error': 'No active carts found for the user'}, status=400)

        line_items = []

        for cart in carts:
            for cart_item in cart.cart_items.all():

                line_items.append({
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(cart_item.get_product_price() * 100),  # amount in cents
                        'product_data': {
                            'name': cart_item.product.product_name,

                        },
                    },
                    'quantity': 1,  # or cart_item.quantity if you have quantity field
                })

        YOUR_DOMAIN = 'http://127.0.0.1:8000/'
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=YOUR_DOMAIN + 'accounts/success/?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=YOUR_DOMAIN + 'accounts/cancel/',
            billing_address_collection='required'

        )

        return JsonResponse({
            'id': checkout_session.id
        })








@login_required
class CustomPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('password_change_done')
    template_name = 'registration/password_change_form.html'



def filter(request):
    # Retrieve all categories
    categories = Category.objects.all()

    # Get the selected category from the request
    selected_category = request.GET.get('category')

    if selected_category:
        # Get the products for the selected category
        products = Product.objects.filter(category__slug=selected_category)
    else:
        # If no category is selected, show all products or handle as needed
        products = Product.objects.all()

    context = {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
    }

    return render(request, 'accounts/filter.html', context)




def search_products(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        products = Product.objects.filter(product_name__icontains=query)
        context = {'products': products}
        return render(request, 'accounts/search.html', context)




def password_reset_done(request):
     return render(request, 'registration/password_reset_done.html')




@login_required 
def profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'accounts/profile.html', {'form': form})





