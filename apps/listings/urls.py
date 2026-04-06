from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('listings/', views.listing_list_view, name='listing_list'),
    path('listings/<int:pk>/', views.listing_detail_view, name='listing_detail'),
    path('listings/create/', views.create_listing_view, name='create_listing'),
    path('listings/<int:pk>/edit/', views.edit_listing_view, name='edit_listing'),
    path('listings/<int:pk>/delete/', views.delete_listing_view, name='delete_listing'),
    path('listings/<int:pk>/wishlist/', views.toggle_wishlist_view, name='toggle_wishlist'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('category/<slug:slug>/', views.listings_by_category_view, name='listings_by_category'),
]
