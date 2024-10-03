from django.contrib import admin

from . import models

admin.site.register(models.Quota)
admin.site.register(models.Package)


