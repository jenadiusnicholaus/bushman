DocType = [
    {"code": "Passport_Copy", "description": "Travel Packet (Passport Copy)"},
    {"code": "Passport_Photo", "description": "Travel Packet (Passport Photo)"},
    {"code": "Visa", "description": "Visa"},
    {"code": "Gun_Permits", "description": "Gun Permits"},
    {"code": "CITES_Documentation", "description": "CITES Documentation"},
]


from django.core.management.base import BaseCommand, CommandError
from sales.models import Doctype


class Command(BaseCommand):
    help = "Create DocType"

    def handle(self, *args, **options):
        for doc in DocType:
            Doctype.objects.create(code=doc["code"], name=doc["description"])
            self.stdout.write(self.style.SUCCESS(f"Creating DocType {doc['code']}"))
