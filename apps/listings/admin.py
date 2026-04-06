from django.contrib import admin
from .models import Category, Listing, ListingImage, Wishlist


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller', 'price', 'condition', 'category', 'is_active', 'is_featured', 'created_at']
    list_filter = ['is_active', 'is_featured', 'condition', 'category']
    search_fields = ['title', 'description', 'seller__username']
    list_editable = ['is_active', 'is_featured']
    inlines = [ListingImageInline]


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'listing', 'created_at']
