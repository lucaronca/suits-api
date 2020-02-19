from django.core.management.base import BaseCommand
from twisted.internet import reactor, defer
from scrapy.settings import Settings
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
import services.scraper.scraper.settings as scraper_settings
from apps.scraped_suits.models import Price
from services.scraper.scraper.spiders.hugo_boss_spiders import (
    HugoBossSuitSpider,
    HugoBossColorSpider,
    HugoBossFitSpider,
    HugoBossMaterialSpider,
    HugoBossPriceSpider,
)


class Command(BaseCommand):
    help = 'Release the spiders'

    def handle(self, *args, **options):
        settings = Settings()
        settings.setmodule(scraper_settings)

        configure_logging(settings=settings)
        runner = CrawlerRunner(settings=settings)

        # prices will be refetched
        Price.objects.all().delete()

        @defer.inlineCallbacks
        def crawl():
            yield runner.crawl(HugoBossSuitSpider)

            runner.crawl(HugoBossColorSpider)
            runner.crawl(HugoBossFitSpider)
            runner.crawl(HugoBossMaterialSpider)
            runner.crawl(HugoBossPriceSpider)

            d = runner.join()
            d.addBoth(lambda _: reactor.stop())

        crawl()
        reactor.run()  # the script will block here until the last crawl call is finished
