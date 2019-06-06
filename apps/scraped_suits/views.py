from rest_framework import generics
from rest_framework.exceptions import APIException
from rest_framework.views import status
from .models import Suit, Price
from .serializers import SuitSerializer
from .filters import SuitFilter
from django.db.models import QuerySet

class BadRequest(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Bad request'
    default_code = 'bad_request'

    def __init__(self, description=None, *args, **kwargs):
        if description is not None:
            self.default_detail = description
        super().__init__()

class ListSuitsView(generics.ListAPIView):
    serializer_class = SuitSerializer

    @staticmethod
    def is_filtering_by_currency(currency, min_price, max_price):
        if currency and not min_price and not max_price:
            suit_ids: QuerySet = Price.objects.filter(currency=currency).values_list('suit_id', flat=True)
            return Suit.objects.filter(url__in=suit_ids)

    def get_queryset(self):
        """
        This view should return a list of all the suits
        currency filter, min_price and max price are handled manually because are custom,
        they manage the prices nested serializer, see serializer.py also.
        """
        currency = self.request.query_params.get('currency')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        self.is_filtering_by_currency(currency, min_price, max_price)

        if min_price or max_price:
            if not currency:
                raise BadRequest('min_price and max_price filters require currency query parameter to be specified')

            if min_price and not max_price:
                suit_ids: QuerySet = Price.objects.filter(
                    currency=currency,
                    amount__gte=min_price
                ).values_list('suit_id', flat=True)

                return Suit.objects.filter(url__in=suit_ids)
            elif max_price and not min_price:
                suit_ids: QuerySet = Price.objects.filter(
                    currency=currency,
                    amount__lte=max_price
                ).values_list('suit_id', flat=True)

                return Suit.objects.filter(url__in=suit_ids)
            elif min_price and max_price:
                suit_ids: QuerySet = Price.objects.filter(
                    currency=currency,
                    amount__gte=min_price,
                    amount__lte=max_price
                ).values_list('suit_id', flat=True)

                return Suit.objects.filter(url__in=suit_ids)

        if currency:
            suit_ids: QuerySet = Price.objects.filter(currency=currency).values_list('suit_id', flat=True)
            return Suit.objects.filter(url__in=suit_ids)

        return Suit.objects.all()