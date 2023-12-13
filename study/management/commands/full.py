from django.core.management import BaseCommand
from study.services import testing


class Command(BaseCommand):
    def handle(self, *args, **options):
        testing()
