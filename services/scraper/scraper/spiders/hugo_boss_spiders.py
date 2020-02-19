import json
import scrapy
from scrapy.http import Request
from ..items import SuitItem, PriceItem
from apps.scraped_suits.models import Suit

BASE_URL = 'https://www.hugoboss.com'
URL_SELECTOR = 'a.product-tile__link::attr(href)'

class HugoBossSuitSpider(scrapy.Spider):
    name = 'hugo_boss'
    start_urls = [BASE_URL + '/boss-men-suits/?sz=999']

    def parse(self, response):
        data = response.css('div.product-tile')

        for line in data:
            item = SuitItem()
            item['url'] = BASE_URL + line.css(URL_SELECTOR).extract_first()
            item['name'] = line.css('div.product-tile__productInfoWrapper::text').extract_first().strip('\n').strip('\n\nby')
            item['image'] = line.css('img.product-tile__image::attr(src)').extract_first()
            yield item

class HugoBossSuitAttributeSpider(scrapy.Spider):
    attribute = None
    value_by_url = None

    def __init__(self, attribute=None, value_by_url=None, *args, **kwargs):
        self.name = 'hugo_boss_{0}'.format(self.attribute)

        if attribute is not None:
            self.attribute = attribute
        elif not getattr(self, 'attribute', None):
            raise ValueError('{0} must have an attribute'.format(type(self).__name__))
        if value_by_url is not None:
            self.value_by_url = value_by_url
        elif not getattr(self, 'value_by_url', None):
            raise ValueError('{0} must have a value_by_url dict'.format(type(self).__name__))

        super().__init__(*args, **kwargs)

    def start_requests(self):
        for url in self.value_by_url:
            yield Request(url=BASE_URL + url, callback=self.parse)
    
    def parse(self, response):
        data = response.css('div.product-tile')

        for line in data:
            item = SuitItem()
            item['url'] = BASE_URL + line.css(URL_SELECTOR).extract_first()
            item[self.attribute] = self.value_by_url[response.url.replace(BASE_URL, '')]
            yield item

class HugoBossColorSpider(HugoBossSuitAttributeSpider):
    attribute = 'color'
    value_by_url = {
        '/men-suits_blue/': 'blue',
        '/men-suits_black/': 'black',
        '/men-suits_grey/': 'grey',
        '/men-suits_beige/': 'beige',
        '/men-suits_brown/': 'brown',
        '/men-suits_pink/': 'pink',
        '/men-suits_white/': 'white',
    }

class HugoBossFitSpider(HugoBossSuitAttributeSpider):
    attribute = 'fit'
    value_by_url = {
        '/men-suits/?prefn1=fit&prefv1=Slim%20fit': 'slim',
        '/men-suits/?prefn1=fit&prefv1=Regular%20fit': 'regular',
        '/men-suits/?prefn1=fit&prefv1=Extra-slim%20fit': 'extra-slim'
    }

class HugoBossMaterialSpider(HugoBossSuitAttributeSpider):
    attribute = 'material'
    value_by_url = {
        '/men-suits/?prefn1=hbMaterialQuality&prefv1=Wool': 'wool',
        '/men-suits/?prefn1=hbMaterialQuality&prefv1=Cotton': 'cotton',
        '/men-suits/?prefn1=hbMaterialQuality&prefv1=Synthetic%20fibre': 'synthetic-fibre',
        '/men-suits/?prefn1=hbMaterialQuality&prefv1=Linen': 'linen'
    }

class HugoBossPriceSpider(scrapy.Spider):
    name = 'hugo_boss_price'
    COUNTRIES_CURRENCY_MAP = {
        'uk': 'GBP',
        'it': 'EUR',
    }
    start_urls = [BASE_URL + '/boss-men-suits/?sz=999']

    @staticmethod
    def make_shop_url_from_standard(country, standard_url):
        return BASE_URL + '/' + country + standard_url

    @staticmethod
    def make_standard_url_from_shop(country, shop_url):
        return shop_url.replace('{}/'.format(country), '')

    def parse(self, response):
        data = response.css('div.product-tile')

        for i, line in enumerate(data):
            suit_link = line.css(URL_SELECTOR).extract_first()

            for country in self.COUNTRIES_CURRENCY_MAP.keys():
                shop_page_url = self.make_shop_url_from_standard(country, suit_link)

                request = scrapy.Request(
                    shop_page_url,
                    meta = {
                        'dont_redirect': True,
                        'handle_httpstatus_list': [301],
                        'cookiejar': i,
                    },
                    callback=self.handle_request
                )
                request.meta['country'] = country

                yield request

    def handle_request(self, response):
        """
        suit_standard_url should be propagated in subsequent 301 redirects (we need the original url), via the meta dict
        when it is not present since is a call at the begin of the stack, we assing it
        """
        try:
            response.meta['suit_standard_url']
        except KeyError:
            response.meta['suit_standard_url'] = self.make_standard_url_from_shop(response.meta['country'], response.url)

        """
        if is a 301 redirect to the moved resource
        """
        if response.status in (301,) and 'Location' in response.headers:
            location = str(response.headers['Location'], 'utf-8')
            self.logger.debug('(parse) Parse page: {} redirecting to Location header: {}'.format(response.url, location))

            request = scrapy.Request(
                location,
                meta = {
                    'dont_redirect': True,
                    'handle_httpstatus_list': [301],
                    'cookiejar': response.meta['cookiejar'],
                },
                callback=self.handle_request
            )
            request.meta['country'] = response.meta['country']
            request.meta['suit_standard_url'] = response.meta['suit_standard_url']

            yield request
        else:
            yield from self.parse_shop_page(response)

    def parse_shop_page(self, response):
        item = PriceItem()
        price_data = response.css('span.product-price::attr(data-pricing)').extract_first()
        item['url'] = response.meta['suit_standard_url']
        item['amount'] = json.loads(price_data)['price']
        item['currency'] = self.COUNTRIES_CURRENCY_MAP[response.meta['country']]

        yield item