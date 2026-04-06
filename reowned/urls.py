from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.listings.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('cart/', include('apps.cart.urls')),
    path('orders/', include('apps.orders.urls')),
    path('messages/', include('apps.inbox.urls')),
    # Static pages
    path('faq/', TemplateView.as_view(template_name='pages/faq.html'), name='faq'),
    path('contact/', TemplateView.as_view(template_name='pages/contact.html'), name='contact'),
    path('privacy-policy/', TemplateView.as_view(template_name='pages/privacy_policy.html'), name='privacy_policy'),
    path('seller-tips/', TemplateView.as_view(template_name='pages/seller_tips.html'), name='seller_tips'),
    path('pricing-guide/', TemplateView.as_view(template_name='pages/pricing_guide.html'), name='pricing_guide'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
