from django.contrib import admin

from sales.models import (
    Entity,
    EntityCategories,
    EntityCategory,
    SalesInquiry,
    ContactType,
    PaymentMethod,
    SalesIquiryPreference,
    SalesInquirySpecies,
    Contacts,
    SalesInquiryArea,
    Document,
    Doctype,
    SalesInquiryPriceList
)
from sales_confirmation.models import SalesQuotaSpeciesStatus

# Register your models here.


admin.site.register(Entity)
admin.site.register(EntityCategories)
admin.site.register(EntityCategory)
admin.site.register(SalesInquiry)
admin.site.register(ContactType)
admin.site.register(PaymentMethod)
admin.site.register(SalesIquiryPreference)
admin.site.register(SalesInquirySpecies)
admin.site.register(Contacts)
admin.site.register(SalesInquiryArea)
admin.site.register(Document)
admin.site.register(Doctype)
admin.site.register(SalesQuotaSpeciesStatus)
admin.site.register(SalesInquiryPriceList)
