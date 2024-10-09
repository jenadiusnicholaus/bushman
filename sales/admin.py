from django.contrib import admin

from sales.models import Entity, EntityCategories, EntityCategory

# Register your models here.


admin.site.register(Entity)
admin.site.register(EntityCategories)
admin.site.register(EntityCategory)
