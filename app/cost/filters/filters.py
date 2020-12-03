from django_filters import rest_framework as filters
from cost import models


class WageCostFilter(filters.FilterSet):
    class Meta:
        model = models.WageCost
        fields = {
            'qty': ['iexact', 'gte', 'lte'],
            'price': ['iexact', 'gte', 'lte'],
        }
