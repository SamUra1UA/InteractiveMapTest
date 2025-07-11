from django_filters import rest_framework as filters
from .models import Location

class LocationFilter(filters.FilterSet):
    min_rating = filters.NumberFilter(method='filter_by_rating')
    category = filters.CharFilter(field_name='category__name', lookup_expr='iexact')

    class Meta:
        model = Location
        fields = ['category']

    def filter_by_rating(self, queryset, name, value):
        return [l for l in queryset if l.average_rating() >= value]
