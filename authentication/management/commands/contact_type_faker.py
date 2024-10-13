from django.core.management.base import BaseCommand
from sales.models import ContactType

CONTACT_TYPE = [
    "email",
    "phone_number",
    "address",
]


class Command(BaseCommand):
    help = "Add Countries"

    def handle(self, *args, **options):
        # country_choices = [{"code": code, "name": name} for code, name in countries]
        for name in CONTACT_TYPE:
            c, created = ContactType.objects.get_or_create(name=name)
            self.stdout.write(self.style.SUCCESS('Added Nationalities "%s"' % name))
