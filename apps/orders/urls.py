from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('', views.order_list_view, name='order_list'),
    path('<int:pk>/', views.order_detail_view, name='order_detail'),
]
