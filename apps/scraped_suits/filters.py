from django_filters import rest_framework as filters
from .models import Suit

class SuitFilter(filters.FilterSet):
    class Meta:
        model = Suit
        fields = ['color', 'fit', 'material']