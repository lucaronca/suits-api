from apps.scraped_suits.models import Suit, Price
from .items import SuitItem, PriceItem


class SuitsPipeline():
    def process_item(self, item, spider):
        if isinstance(item, SuitItem):
            return self.handle_suit(item, spider)
        if isinstance(item, PriceItem):
            return self.handle_price(item, spider)

        raise Exception('item of {} Class is not handled by {}'.format(type(item).__name__, self.__class__.__name__))

    def handle_suit(self, item, spider):
        try:
            # suit already exits
            suit = Suit.objects.get(pk=item['url'])
            field_to_update = []

            # attribute spiders
            if item.get('color'):
                suit.color = item['color']
                field_to_update.append('color')
            if item.get('fit'):
                suit.fit = item['fit']
                field_to_update.append('fit')
            if item.get('material'):
                suit.material = item['material']
                field_to_update.append('material')

            # update the model if pipeline processed an attribute spider
            if field_to_update != None:
                suit.save(update_fields=field_to_update)

        except Suit.DoesNotExist:
            item.save() # save instantiates the django model and save it

        finally:
            return item

    def handle_price(self, item, spider):
        suit = Suit.objects.get(pk=item['url'])
        price = Price(suit=suit, amount=item.get('amount'), currency=item.get('currency'))
        price.save()
        return item
