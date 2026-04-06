from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('add/<int:pk>/', views.add_to_cart_view, name='add_to_cart'),
    path('remove/<int:pk>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('clear/', views.clear_cart_view, name='clear_cart'),
]
