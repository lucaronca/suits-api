from django.urls import reverse
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from rest_framework.views import status, APIView
from rest_framework.exceptions import ErrorDetail
from .models import Suit, Price
from .serializers import SuitSerializer


class BaseViewTest(APITestCase):
    client = APIClient()
    request_factory = APIRequestFactory()  # every test needs access to the request factory.

    @staticmethod
    def create_suit(url='', name='', color='', fit='', material='', image=''):
        if url != '' and name != '' and color != '' and fit != '' and material != '' and image != '':
            return Suit.objects.create(url=url, name=name, color=color, fit=fit, material=material, image=image)

    @staticmethod
    def create_price(suit=None, amount='', currency=''):
        if suit is not None and amount != '' and currency != '':
            return Price.objects.create(suit=suit, amount=amount, currency=currency)

    def get_request(self, endpoint):
        # create an instance of a GET request.
        raw_request = self.request_factory.get(endpoint)
        drf_request = APIView().initialize_request(raw_request)
        return drf_request

    def setUp(self):
        # add test data

        # suits
        suit_1 = self.create_suit('test_url_1', 'test_suit_1', 'blue', 'slim', 'wool', 'test-image')
        suit_2 = self.create_suit('test_url_2', 'test_suit_2', 'black', 'regular', 'wool', 'test-image')
        suit_3 = self.create_suit('test_url_3', 'test_suit_3', 'grey', 'slim', 'extra-slim', 'test-image')
        self.create_suit('test_url_4', 'test_suit_4', 'brown', 'slim', 'wool', 'test-image')

        # prices
        self.create_price(suit_1, '123.00', 'GBP')
        self.create_price(suit_1, '123.00', 'EUR')
        self.create_price(suit_2, '130.00', 'GBP')
        self.create_price(suit_3, '1350.00', 'GBP')


class GetAllSuitsTest(BaseViewTest):

    def assert_by_endpoint(self, endpoint, expected):
        request = self.get_request(endpoint)

        # hit the API endpoint
        response = self.client.get(endpoint)

        # serialize db data
        expected_serialized = SuitSerializer(expected, many=True, context={'request': request})

        self.assertEqual(response.data['results'], expected_serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_suits(self):
        """
        This test ensures that all suits added in the setUp method
        exist when we make a GET request to the suits/ endpoint
        """

        # fetch the data from db
        expected = Suit.objects.all()

        self.assert_by_endpoint(
            reverse('list-suits', kwargs={'version': 'v1'}),
            expected
        )

    def test_get_all_suits_filtered_by_currency(self):
        """
        This test ensures that all suits added in the setUp method
        are filtered by currency when we make a GET request to the suits/ endpoint
        passing the currency as a queryparameter
        """

        expected_GBP = Suit.objects.filter(pk__in=['test_url_1', 'test_url_2', 'test_url_3'])

        self.assert_by_endpoint(
            reverse('list-suits', kwargs={'version': 'v1'}) + '?currency=GBP',
            expected_GBP
        )

        expected_EUR = Suit.objects.filter(pk__in=['test_url_1'])

        self.assert_by_endpoint(
            reverse('list-suits', kwargs={'version': 'v1'}) + '?currency=EUR',
            expected_EUR
        )

    def test_get_all_suits_filtered_by_max_price(self):
        """
        This test ensures that all suits added in the setUp method
        are filtered by max_price when we make a GET request to the suits/ endpoint
        passing the max_price as a queryparameter
        """

        api_url = reverse('list-suits', kwargs={'version': 'v1'})

        self.assert_by_endpoint(
            api_url + '?currency=GBP&max_price=125.00',
            Suit.objects.filter(pk='test_url_1')
        )

        self.assert_by_endpoint(
            api_url + '?currency=GBP&max_price=130.00',
            Suit.objects.filter(pk__in=['test_url_1', 'test_url_2'])
        )

        self.assert_by_endpoint(
            api_url + '?currency=EUR&max_price=130.00',
            Suit.objects.filter(pk='test_url_1')
        )

    def test_get_all_suits_filtered_by_max_price_without_currency(self):
        """
        This test ensures that when we make a GET request to the suits/ endpoint
        passing the max_price as a queryparam without a the currency queryparam
        a 400 bad request error is returned
        """

        endpoint = reverse('list-suits', kwargs={'version': 'v1'}) + '?max_price=125.00'

        # hit the API endpoint
        response = self.client.get(endpoint)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data['detail'], ErrorDetail)

    def test_get_all_suits_filtered_by_min_price(self):
        """
        This test ensures that all suits added in the setUp method
        are filtered by min_price when we make a GET request to the suits/ endpoint
        passing the max_price as a queryparameter
        """

        api_url = reverse('list-suits', kwargs={'version': 'v1'})

        self.assert_by_endpoint(
            api_url + '?currency=GBP&min_price=1000.00',
            Suit.objects.filter(pk='test_url_3')
        )

        self.assert_by_endpoint(
            api_url + '?currency=GBP&min_price=124.00',
            Suit.objects.filter(pk__in=['test_url_2', 'test_url_3'])
        )

        self.assert_by_endpoint(
            api_url + '?currency=EUR&min_price=120.00',
            Suit.objects.filter(pk='test_url_1')
        )

    def test_get_all_suits_filtered_by_min_price_without_currency(self):
        """
        This test ensures that when we make a GET request to the suits/ endpoint
        passing the min_price as a queryparam without a the currency queryparam
        a 400 bad request error is returned
        """

        endpoint = reverse('list-suits', kwargs={'version': 'v1'}) + '?min_price=125.00'

        # hit the API endpoint
        response = self.client.get(endpoint)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data['detail'], ErrorDetail)
