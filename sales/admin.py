from django.contrib import admin

from sales.models import (
    Entity,
    EntityCategories,
    EntityCategory,
    SalesInquiry,
    ContactType,
    PaymentMethod,
)

# Register your models here.


admin.site.register(Entity)
admin.site.register(EntityCategories)
admin.site.register(EntityCategory)
admin.site.register(SalesInquiry)
admin.site.register(ContactType)
admin.site.register(PaymentMethod)
