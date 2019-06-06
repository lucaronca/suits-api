import scrapy
from scrapy_djangoitem import DjangoItem
from apps.scraped_suits.models import Suit, Price


class SuitItem(DjangoItem):
    django_model = Suit

class PriceItem(DjangoItem):
    django_model = Price
    url = scrapy.Field()