from django.core.management.base import BaseCommand, CommandError

from bm_hunting_settings.models import QuotaHuntingAreaSpecies

# import F
from django.db.models import F


# QuotaHuntingAreaSpecies
class Command(BaseCommand):
    help = "Updates the species quantity in the quota table"

    def handle(self, *args, **options):
        # Get all records where quantity is less than 5
        qs = QuotaHuntingAreaSpecies.objects.filter(quantity__lt=5)
        print(len(qs))
        if len(qs) == 0:
            self.stdout.write(
                self.style.WARNING("No records found with quantity less than 5")
            )
            return
        # Update the quantity by adding 10 to each affected record
        updated_count = qs.update(quantity=F("quantity") + 10)

        # Output success message with the number of updated records
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully updated {updated_count} species quantity in the quota table"
            )
        )
