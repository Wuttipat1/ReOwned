import django_filters
from .models import Listing, Category


class ListingFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Min Price')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='Max Price')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    condition = django_filters.MultipleChoiceFilter(choices=Listing.CONDITION_CHOICES)
    brand = django_filters.CharFilter(lookup_expr='icontains')
    search = django_filters.CharFilter(method='search_filter', label='Search')

    class Meta:
        model = Listing
        fields = ['category', 'condition', 'brand', 'min_price', 'max_price']

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            title__icontains=value
        ) | queryset.filter(
            description__icontains=value
        ) | queryset.filter(
            brand__icontains=value
        )
