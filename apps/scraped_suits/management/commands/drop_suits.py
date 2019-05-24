from django.core.management.base import BaseCommand
from apps.scraped_suits.models import Suit

class Command(BaseCommand):
    help = 'Drop all suits in the database'

    def handle(self, *args, **options):
        Suit.objects.all().delete()
        print('All suits have been dropped')