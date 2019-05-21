from apps.scraped_suits.models import Suit


class SuitPipeline():
    def process_item(self, item, spider):
        try:
            # suit already exits
            suit = Suit.objects.get(url=item["url"])
            fields_to_update = []
            if item.get('color', None) != None:
                fields_to_update.append('color')
                suit.color = item['color']
            if item.get('fit', None) != None:
                fields_to_update.append('fit')
                suit.fit = item['fit']
            if item.get('material', None) != None:
                fields_to_update.append('material')
                suit.material = item['material']
            suit.save(update_fields=fields_to_update)
            return item
        except Suit.DoesNotExist:
            pass

        item.save() # save instantiates the django model already making a save on it  
        return item