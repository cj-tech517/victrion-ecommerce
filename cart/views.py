from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import CartItem
from products.models import Product
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages



# Create your views here.


def cart_detail(request):
    if request.user.is_authenticated:
        items = CartItem.objects.filter(user=request.user)
    else:
        items = CartItem.objects.filter(session_key=request.session.session_key)

    total = sum([item.total_price() for item in items])
    return render(request, 'cart_detail.html', {'items': items, 'total': total})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if not request.session.session_key:
        request.session.create()

    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    else:
        cart_item, created = CartItem.objects.get_or_create(session_key=request.session.session_key, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')

def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart_detail')


def update_cart_quantity(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        product = cart_item.product

        try:
            new_quantity = int(request.POST.get('quantity', 1))

            if new_quantity < 1:
                cart_item.delete()
                return redirect('cart_detail')

            if new_quantity > product.stock:
                messages.error(
                    request,
                    f"Only {product.stock} item(s) available in stock."
                )
                new_quantity = product.stock

            cart_item.quantity = new_quantity
            cart_item.save()

        except ValueError:
            pass

    return redirect('cart_detail')

