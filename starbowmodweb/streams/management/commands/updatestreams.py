from django.core.management.base import BaseCommand
from starbowmodweb.streams.getstreamstatus import update_stream_cache


class Command(BaseCommand):
    help = 'Updates the stream information (online/offline, viewers)'

    def handle(self, *args, **options):
        update_stream_cache()
        self.stdout.write('Updated the stream information')