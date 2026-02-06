from django.shortcuts import render
from django.shortcuts import render, redirect
from cart.models import CartItem
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# Create your views here.




@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        return redirect('home')

    total = sum([item.total_price() for item in cart_items])

    if request.method == 'POST':
        # Create order
        order = Order.objects.create(user=request.user, total=total)
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        # Clear cart
        cart_items.delete()
        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'checkout.html', {'cart_items': cart_items, 'total': total})



@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_confirmation.html', {'order': order})
