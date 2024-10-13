from django_countries import countries
from django.core.management.base import BaseCommand
from bm_hunting_settings.models import Country


class Command(BaseCommand):
    help = "Add Countries"

    # def add_arguments(self, parser):
    #     parser.add_argument("Nationalities_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        # country_choices = [{"code": code, "name": name} for code, name in countries]
        for code, name in countries:
            c, created = Country.objects.get_or_create(code=code, name=name)
            self.stdout.write(self.style.SUCCESS('Added Nationalities "%s"' % name))
