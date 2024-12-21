from products.models import Product, ProductRentalPrice
import django_filters
from django.db.models import Exists, OuterRef
from django_filters import OrderingFilter

class ProductFilter(django_filters.FilterSet):
    is_rent = django_filters.BooleanFilter(method='filter_is_rent', label='Rent')
    price_order = django_filters.ChoiceFilter(
        choices=[('asc', 'Ascending'), ('desc', 'Descending')],
        method='filter_price_order',
        label='Order by price'
    )

    class Meta:
        model = Product
        fields = ['is_rent', 'price_order']

    def filter_is_rent(self, queryset, name, value):
        # Sadece aktif ürünleri getirelim
        queryset = queryset.filter(is_active=True)

        if value is None:
            return queryset

        elif value:
            return queryset.annotate(
                has_rental_price=Exists(ProductRentalPrice.objects.filter(product=OuterRef('pk')))
            ).filter(has_rental_price=True)

        else:
            return queryset.annotate(
                has_rental_price=Exists(ProductRentalPrice.objects.filter(product=OuterRef('pk')))
            ).filter(has_rental_price=False)

    def filter_price_order(self, queryset, name, value):
        queryset = queryset.filter(is_active=True)

        if value == 'asc':
            return queryset.order_by('selling_price')
        elif value == 'desc':
            return queryset.order_by('-selling_price')
        return queryset
