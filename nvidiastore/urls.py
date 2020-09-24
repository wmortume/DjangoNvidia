from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup, name='signup'),
    path('login', views.signin, name='login'),
    path('logout', views.signout, name='logout'),
    path('home', views.home, name='home'),
    path('order/<str:product_url>', views.order, name='order'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout')
]
