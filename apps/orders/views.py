from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from apps.cart.models import Cart


@login_required
def checkout_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')
    if request.method == 'POST':
        address = request.POST.get('shipping_address', '').strip()
        if not address:
            messages.error(request, 'Please provide a shipping address.')
            return render(request, 'orders/checkout.html', {'cart': cart})
        order = Order.objects.create(
            buyer=request.user,
            total_amount=cart.total,
            shipping_address=address,
        )
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                listing=item.listing,
                title=item.listing.title,
                price=item.listing.price,
                quantity=item.quantity,
            )
        cart.items.all().delete()
        messages.success(request, f'Order #{order.pk} placed successfully!')
        return redirect('order_detail', pk=order.pk)
    return render(request, 'orders/checkout.html', {'cart': cart})


@login_required
def order_list_view(request):
    orders = Order.objects.filter(buyer=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail_view(request, pk):
    order = get_object_or_404(Order, pk=pk, buyer=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
