from django.core.management.base import BaseCommand

from exo_currency.models import Provider
from exo_currency.utils import CURRENCY_EXCHANGER_PROVIDERS


class Command(BaseCommand):
    help = """Load providers."""

    def handle(self, *args, **options):
        order = 1
        for _name, _class in CURRENCY_EXCHANGER_PROVIDERS:
            Provider.objects.update_or_create(
                name=_name,
                defaults={
                    'order': order,
                }
            )
            order += 1
