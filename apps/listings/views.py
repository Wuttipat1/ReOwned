from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Listing, Category, Wishlist
from .filters import ListingFilter
from .forms import ListingForm, ListingImageFormSet


def home_view(request):
    featured = Listing.objects.filter(is_active=True, is_featured=True)[:8]
    latest = Listing.objects.filter(is_active=True)[:8]
    categories = Category.objects.all()
    return render(request, 'listings/home.html', {
        'featured': featured,
        'latest': latest,
        'categories': categories,
    })


def listing_list_view(request):
    queryset = Listing.objects.filter(is_active=True)
    f = ListingFilter(request.GET, queryset=queryset)
    paginator = Paginator(f.qs, 12)
    listings = paginator.get_page(request.GET.get('page'))
    categories = Category.objects.all()
    return render(request, 'listings/listing_list.html', {
        'listings': listings,
        'filter': f,
        'categories': categories,
    })


def listing_detail_view(request, pk):
    listing = get_object_or_404(Listing, pk=pk, is_active=True)
    listing.views_count += 1
    listing.save(update_fields=['views_count'])
    related = Listing.objects.filter(
        category=listing.category, is_active=True
    ).exclude(pk=pk)[:4]
    is_wishlisted = False
    if request.user.is_authenticated:
        is_wishlisted = Wishlist.objects.filter(user=request.user, listing=listing).exists()
    return render(request, 'listings/listing_detail.html', {
        'listing': listing,
        'related': related,
        'is_wishlisted': is_wishlisted,
    })


def listings_by_category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    queryset = Listing.objects.filter(is_active=True, category=category)
    f = ListingFilter(request.GET, queryset=queryset)
    paginator = Paginator(f.qs, 12)
    listings = paginator.get_page(request.GET.get('page'))
    return render(request, 'listings/listing_list.html', {
        'listings': listings,
        'filter': f,
        'category': category,
        'categories': Category.objects.all(),
    })


@login_required
def create_listing_view(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        formset = ListingImageFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            formset.instance = listing
            formset.save()
            messages.success(request, 'Listing created!')
            return redirect(listing.get_absolute_url())
    else:
        form = ListingForm()
        formset = ListingImageFormSet()
    return render(request, 'listings/create_listing.html', {'form': form, 'formset': formset})


@login_required
def edit_listing_view(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    if request.method == 'POST':
        form = ListingForm(request.POST, instance=listing)
        formset = ListingImageFormSet(request.POST, request.FILES, instance=listing)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Listing updated!')
            return redirect(listing.get_absolute_url())
    else:
        form = ListingForm(instance=listing)
        formset = ListingImageFormSet(instance=listing)
    return render(request, 'listings/create_listing.html', {
        'form': form, 'formset': formset, 'listing': listing
    })


@login_required
def delete_listing_view(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    if request.method == 'POST':
        listing.is_active = False
        listing.save()
        messages.success(request, 'Listing removed.')
        return redirect('profile')
    return render(request, 'listings/confirm_delete.html', {'listing': listing})


@login_required
def toggle_wishlist_view(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    listing = get_object_or_404(Listing, pk=pk)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, listing=listing)
    if not created:
        wishlist.delete()
        saved = False
    else:
        saved = True
    return JsonResponse({'saved': saved})


@login_required
def wishlist_view(request):
    wishlist = Wishlist.objects.filter(user=request.user).select_related('listing')
    return render(request, 'listings/wishlist.html', {'wishlist': wishlist})
