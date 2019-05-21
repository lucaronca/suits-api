from scrapy_djangoitem import DjangoItem
from apps.scraped_suits.models import Suit


class SuitItem(DjangoItem):
    django_model = Suit