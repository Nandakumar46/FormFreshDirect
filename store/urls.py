# store/urls.py
from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:product_id>/', views.edit_product, name='edit_product'),

    # THIS IS THE CORRECT URL FOR UNLISTING
    path('products/unlist/<int:product_id>/', views.unlist_product, name='unlist_product'),

    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
]