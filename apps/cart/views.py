from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem
from apps.listings.models import Listing


@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/cart.html', {'cart': cart})


@login_required
def add_to_cart_view(request, pk):
    listing = get_object_or_404(Listing, pk=pk, is_active=True)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, listing=listing)
    if not created:
        item.quantity += 1
        item.save()
    messages.success(request, f'"{listing.title}" added to cart!')
    return redirect(request.META.get('HTTP_REFERER', 'cart'))


@login_required
def remove_from_cart_view(request, pk):
    cart = get_object_or_404(Cart, user=request.user)
    CartItem.objects.filter(cart=cart, listing_id=pk).delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart')


@login_required
def clear_cart_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()
    return redirect('cart')
