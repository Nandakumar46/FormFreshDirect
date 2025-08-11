# store/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from .models import Product, Cart, CartItem, Order, OrderItem, ShippingAddress
from .forms import ProductForm, AddressForm

def home(request):
    return render(request, 'home.html')

def product_list(request):
    # This shows only available products
    products = Product.objects.filter(is_available=True).order_by('-created_at')
    return render(request, 'store/product_list.html', {'products': products})

@login_required
def add_product(request):
    if request.user.profile.user_type != 'FARMER':
        return redirect('store:product_list')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.farmer = request.user
            product.save()
            return redirect('store:product_list')
    else:
        form = ProductForm()
    return render(request, 'store/product_form.html', {'form': form})

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.farmer != request.user:
        messages.error(request, "You are not authorized to edit this product.")
        return redirect('store:product_list')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{product.name}" has been updated successfully.')
            return redirect('store:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/product_form.html', {'form': form, 'is_edit': True})

# THIS IS THE CORRECT FUNCTION TO UNLIST A PRODUCT
@login_required
def unlist_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.farmer != request.user:
        messages.error(request, "You are not authorized to modify this product.")
        return redirect('store:product_list')
    if request.method == 'POST':
        product.is_available = False # This is the key change!
        product.save()
        messages.success(request, f'Product "{product.name}" has been unlisted.')
        return redirect('store:product_list')
    return redirect('store:product_list')

# --- All the cart and order views below ---
@login_required
def add_to_cart(request, product_id):
    # ... (existing code)
    if request.user.profile.user_type != 'CLIENT':
        messages.error(request, 'Only clients can add items to the cart.')
        return redirect('store:product_list')
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'Added another "{product.name}" to your cart.')
    else:
        messages.success(request, f'"{product.name}" has been added to your cart.')
    return redirect('store:product_list')

@login_required
def view_cart(request):
    # ... (existing code)
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
        total_price = sum(item.total_price for item in cart_items)
    except Cart.DoesNotExist:
        cart_items = []
        total_price = 0
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def checkout(request):
    # ... (existing code)
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
        if not cart_items:
            messages.error(request, 'Your cart is empty.')
            return redirect('store:view_cart')
    except Cart.DoesNotExist:
        messages.error(request, 'You do not have a cart.')
        return redirect('store:product_list')
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            total_price = sum(item.total_price for item in cart_items)
            order = Order.objects.create(
                user=request.user,
                shipping_address=address,
                total_price=total_price
            )
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )
            cart.items.all().delete()
            subject = f'Your FarmFreshDirect Order #{order.id} is confirmed!'
            html_message = render_to_string('emails/order_confirmation.html', {'user': request.user, 'order': order})
            plain_message = f"Hi {request.user.username}, Your order #{order.id} for ₹{order.total_price} is confirmed."
            send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [request.user.email], html_message=html_message)
            return redirect('store:order_success', order_id=order.id)
    else:
        form = AddressForm()
    return render(request, 'store/checkout.html', {'form': form})

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_success.html', {'order': order})