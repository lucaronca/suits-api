import scrapy
from scrapy.http import Request
from ..items import SuitItem

class HugoBossSuitSpider(scrapy.Spider):
    name = 'hugo_boss'
    BASE_URL = 'https://www.hugoboss.com'
    start_urls = ['https://www.hugoboss.com/boss-men-suits/']

    def parse(self, response):
        data = response.css('div.product-tile')

        for line in data:
            item = SuitItem()
            item['url'] = self.BASE_URL + line.css('a.product-tile__link::attr(href)').extract_first()
            item['name'] = line.css('div.product-tile__productInfoWrapper::text').extract_first()
            item['image'] = line.css('img.product-tile__image::attr(src)').extract_first()
            yield item

class HugoBossSuitAttributeSpider(scrapy.Spider):
    BASE_URL = 'https://www.hugoboss.com'
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
            yield Request(url=self.BASE_URL + url, callback=self.parse)
    
    def parse(self, response):
        data = response.css('div.product-tile')

        for line in data:
            item = SuitItem()
            item['url'] = self.BASE_URL + line.css('a.product-tile__link::attr(href)').extract_first()
            item[self.attribute] = self.value_by_url[response.url.replace(self.BASE_URL, '')]
            yield item

class HugoBossColorSpider(HugoBossSuitAttributeSpider):
    attribute = 'color'
    value_by_url = {
        '/boss-men-suits_blue/': 'blue',
        '/boss-men-suits_black/': 'black',
        '/boss-men-suits_grey/': 'grey',
        '/boss-men-suits_beige/': 'beige',
        '/boss-men-suits_brown/': 'brown',
        '/boss-men-suits_pink/': 'pink',
        '/boss-men-suits_white/': 'white',
    }

class HugoBossFitSpider(HugoBossSuitAttributeSpider):
    attribute = 'fit'
    value_by_url = {
        '/boss-men-suits/?prefn1=fit&prefv1=Slim%20fit': 'slim',
        '/boss-men-suits/?prefn1=fit&prefv1=Regular%20fit': 'regular',
        '/boss-men-suits/?prefn1=fit&prefv1=Extra-slim%20fit': 'extra-slim'
    }

class HugoBossMaterialSpider(HugoBossSuitAttributeSpider):
    attribute = 'material'
    value_by_url = {
        '/boss-men-suits/?prefn1=hbMaterialQuality&prefv1=Wool': 'wool',
        '/boss-men-suits/?prefn1=hbMaterialQuality&prefv1=Cotton': 'cotton',
        '/boss-men-suits/?prefn1=hbMaterialQuality&prefv1=Synthetic%20fibre': 'synthetic-fibre',
        '/boss-men-suits/?prefn1=hbMaterialQuality&prefv1=Linen': 'linen'
    }
