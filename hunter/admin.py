from django.contrib import admin
from .models import Client, Weapon, HunterItinerary, ClientDocument
from bm_hunting_settings.models import  HuntingBlock, Species, HuntingType, SafariPackageType

admin.site.register(Client)
admin.site.register(HuntingBlock)
admin.site.register(Species)
admin.site.register(HuntingType)
admin.site.register(SafariPackageType)
admin.site.register(Weapon)
admin.site.register(HunterItinerary)
admin.site.register(ClientDocument)

