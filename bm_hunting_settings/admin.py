from django.contrib import admin

from . import models

admin.site.register(models.Quota)
admin.site.register(models.Nationalities)
# admin.site.register(models.Species)
admin.site.register(models.HuntingArea)
admin.site.register(models.HuntingQuatasArea)
admin.site.register(models.QuotaHutingAreaSpecies)
