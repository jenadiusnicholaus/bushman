# AccommodationType
from django.core.management.base import BaseCommand, CommandError
from bm_hunting_settings.models import AccommodationType


class Command(BaseCommand):
    help = "Create accommodation types"

    def handle(self, *args, **options):
        ACCOMMODATION_LIST = [
            "Hotel",
            "Apartment",
            "Hostel",
            "Guesthouse",
            "B&B",
            "Luxury Tent",
        ]

        for accommodation in ACCOMMODATION_LIST:
            accommodation_type = AccommodationType(name=accommodation)
            accommodation_type.save()
            self.stdout.write(
                self.style.SUCCESS(f"Accommodation type {accommodation} created")
            )
