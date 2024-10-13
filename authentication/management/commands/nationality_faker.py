from django.core.management.base import BaseCommand, CommandError
from bm_hunting_settings.models import Nationalities
from settings.settings import NATIONALITIES


class Command(BaseCommand):
    help = "Closes the specified Nationalities for voting"

    # def add_arguments(self, parser):
    #     parser.add_argument("Nationalities_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        for name in NATIONALITIES:
            try:
                nationalities, created = Nationalities.objects.get_or_create(name=name)
            except Nationalities.DoesNotExist:
                raise CommandError('Nationalities "%s" does not exist' % name)


            self.stdout.write(self.style.SUCCESS('Added Nationalities "%s"' % name))
