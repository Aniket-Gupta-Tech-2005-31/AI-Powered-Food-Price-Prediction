from django.core.management.base import BaseCommand
from api.tasks import fetch_and_store_prices


class Command(BaseCommand):
    help = 'Fetch latest prices using configured scrapers. Use --async to enqueue as a Celery task.'

    def add_arguments(self, parser):
        parser.add_argument('--async', action='store_true', dest='use_async', help='Enqueue the fetch task to Celery instead of running synchronously')

    def handle(self, *args, **options):
        use_async = options.get('use_async', False)
        if use_async:
            result = fetch_and_store_prices.delay()
            self.stdout.write(self.style.SUCCESS(f'Enqueued fetch task: {result.id}'))
        else:
            self.stdout.write('Running fetch task synchronously...')
            result = fetch_and_store_prices()
            self.stdout.write(self.style.SUCCESS(f'Done: {result}'))
