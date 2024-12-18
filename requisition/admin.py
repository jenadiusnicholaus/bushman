from django.contrib import admin

# Register your models here.

from .models import (
    Requisition,
    RequestItem,
    RequestItemAccount,
    RequestItemItems,
    RequestItemSource,
)

admin.site.register(Requisition)
admin.site.register(RequestItem)
admin.site.register(RequestItemAccount)
admin.site.register(RequestItemItems)
admin.site.register(RequestItemSource)
admin.site.site_header = "Bushman Requisition"
