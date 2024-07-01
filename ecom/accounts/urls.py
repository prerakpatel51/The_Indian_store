from django.urls import path,include
from accounts.views import login_page,register_page , activate_email
from .views import *
from django.contrib.auth import views as auth_views
urlpatterns = [
   path('login/' , login_page , name="login" ),
   path('register/' , register_page , name="register"),
   path('logout/', logout_view, name='logout'),
  
   path('activate/<email_token>/' , activate_email , name="activate_email"),
   
   path('add_to_cart/<uid>/',add_to_cart,name='add_to_cart'),
   path('cart',cart,name="cart"),
   path('remove_cart/<cart_item_uid>/',remove_cart,name='remove_cart'),
   path('remove_coupon/<cart_id>/',remove_coupon,name='remove_coupon'),
   
   path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
   
   path('success/', success_view, name='success'),
   path('track_status/',track_status,name='track_status'),
   path('cancel/', cancel_view, name='cancel'),
   
   path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
  #  path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
   path('password_reset/done/', password_reset_done, name='password_reset_done'),
   
   path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
   path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

  path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    # path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_change/done/', password_change_done, name='password_change_done'),
    
    path('filter_products/',filter,name='filter_products'),
    path('search/',search_products,name='search'),
     
     path('profile',profile,name='profile'),
     
    
]



