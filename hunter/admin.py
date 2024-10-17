from django.contrib import admin
from .models import (
    Client,
    Weapon,
    clientItinerary,
    # ClientDocument,
    # ClientSalesOrder,
    Observer,
    Companion,
    # Entity,
    # EntityCategories,
    # EntityCategory,
)
from bm_hunting_settings.models import (
    # HuntingBlock,
    Species,
    HuntingType,
    # RegulatoryHuntingpackage,
)

# admin.site.register(Client)
# admin.site.register(HuntingBlock)
# admin.site.register(HuntingType)
# admin.site.register(SafariPackageType)
admin.site.register(Weapon)
admin.site.register(clientItinerary)
# admin.site.register(ClientDocument)
# admin.site.register(ClientSalesOrder)
# admin.site.register(Observer)
# admin.site.register(Companion)
# admin.site.register(Entity)
# admin.site.register(EntityCategories)
# admin.site.register(EntityCategory)
