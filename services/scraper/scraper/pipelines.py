from apps.scraped_suits.models import Suit


class SuitPipeline():
    def process_item(self, item, spider):
        try:
            # suit already exits
            suit = Suit.objects.get(pk=item['url'])
            field_to_update = None

            # attribute spiders
            if item.get('color', None) != None:
                suit.color = item['color']
                field_to_update = 'color'
            if item.get('fit', None) != None:
                suit.fit = item['fit']
                field_to_update = 'fit'
            if item.get('material', None) != None:
                suit.material = item['material']
                field_to_update = 'material'

            # update the model if pipeline has processed an attribute spider
            if field_to_update != None:
                suit.save(update_fields=[field_to_update])

        except Suit.DoesNotExist:
            item.save() # save instantiates the django model and save it

        finally:
            return item
