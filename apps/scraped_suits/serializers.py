from rest_framework import serializers
from .models import Suit, Price


class FilteredPriceListSerializer(serializers.ListSerializer):
    def get_query_param(self, query_param: str):
        return self.context['request'].query_params.get(query_param)

    """
        here are handled currency, min_price, max_price filters
    """
    def to_representation(self, data):
        currency = self.get_query_param('currency')
        min_price = self.get_query_param('min_price')
        max_price = self.get_query_param('max_price')

        if currency and not min_price and not max_price:
            data = data.filter(currency=currency)

        if min_price and not max_price:
            data = data.filter(currency=currency, amount__gte=min_price)

        if max_price and not min_price:
            data = data.filter(currency=currency, amount__lte=max_price)

        if min_price and max_price:
            data = data.filter(currency=currency, amount__gte=min_price, amount__lte=max_price)

        return super(FilteredPriceListSerializer, self).to_representation(data)


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = FilteredPriceListSerializer
        model = Price
        fields = ('amount', 'currency')


class SuitSerializer(serializers.ModelSerializer):
    prices = PriceSerializer(read_only=True, many=True, source='price_set')

    class Meta:
        model = Suit
        fields = ('url', 'name', 'color', 'fit', 'material', 'image', 'prices')
