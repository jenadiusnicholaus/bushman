#


from django.core.management.base import BaseCommand, CommandError
from sales.models import Doctype
from sales_confirmation.models import SalesQuotaSpeciesStatus
from utils.utitlities import currentQuuta


class Command(BaseCommand):
    help = "Create DocType"

    def handle(self, *args, **options):
        current_quota = currentQuuta.current_quota
        # for doc in DocType:
        #     Doctype.objects.create(code=doc["code"], name=doc["description"])
        #     self.stdout.write(self.style.SUCCESS(f"Creating DocType {doc['code']}"))
        # get all species status with null quota field the update to curent quota value
        null_quota_species_status = SalesQuotaSpeciesStatus.objects.filter(quota=None)
        if null_quota_species_status.exists():

            for status in null_quota_species_status:
                status.quota = current_quota
                status.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Updating species status {status.species} to current quota {current_quota}"
                    )
                )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"All species status already have current quota {current_quota}"
                )
            )
