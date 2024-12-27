unit_of_measurements = [
    ("KGS", "Kg", ""),
    ("LITERS", "lts", ""),
    ("NOS", "nos", ""),
    ("SET", "set", ""),
    ("METERS", "M", ""),
    ("EACH", "EACH", ""),
    ("PIECE", "PIECE", ""),
    ("BUNDLES", "BUNDLES", ""),
    ("BAGS", "BAGS", ""),
    ("PALLETS", "PALLETS", ""),
    ("PECK", "PECK", ""),
    ("Cubic Meters", "M3", ""),
    ("CN", "CN", ""),
    ("ITEM(S)", "ITEM(S)", ""),
    ("PACKET(S)", "PACKET(S)", ""),
    ("BOTTLE(S)", "BOTTLE(S)", ""),
    ("REAM(S)", "REAM(S)", ""),
    ("ROLL(S)", "ROLL(S)", ""),
    ("GALON", "GALON", ""),
]

from django.core.management.base import BaseCommand, CommandError
from bm_hunting_settings.models import UnitOfMeasurements


class Command(BaseCommand):
    def human_readable_unit(self, unit):
        for uom in unit_of_measurements:
            if unit.upper() == uom[0]:
                return uom[1]
        return unit

    def handle(self, *args, **options):
        for uom in unit_of_measurements:
            unit, created = UnitOfMeasurements.objects.get_or_create(
                name=uom[0],
                unit=uom[1],
            )

            self.stdout.write(
                self.style.SUCCESS(f"Created unit of measurement {uom[1]}")
            )
