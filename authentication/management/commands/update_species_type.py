from bm_hunting_settings.models import Species
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Updates species type"

    def handle(self, *args, **options):
        # get all species  and check where the type is null he update it "NORMAL"
        count_updated = 0

        try:
            species = Species.objects.filter(type__isnull=True)
            for s in species:
                s.type = "NORMAL"
                s.save()
                count_updated += 1

            if count_updated == 0:
                self.stdout.write(self.style.WARNING("No species type updated"))
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"{count_updated} Species updated type successfully "
                    )
                )
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
            self.stdout.write(
                self.style.ERROR("Error occurred while updating species type")
            )
            raise CommandError(e)
