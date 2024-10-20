from django.contrib import admin

from . import models

admin.site.register(models.Quota)
admin.site.register(models.Nationalities)
admin.site.register(models.Species)
admin.site.register(models.HuntingArea)
admin.site.register(models.HuntingQuatasArea)
admin.site.register(models.QuotaHutingAreaSpecies)
# RegulatoryHuntingpackage
admin.site.register(models.RegulatoryHuntingpackage)
# RegulatoryHuntingPackageSpecies
admin.site.register(models.RegulatoryHuntingPackageSpecies)
# GeoLocationCoordinates
admin.site.register(models.GeoLocationCoordinates)
admin.site.register(models.Locations)

# SalesPackage
admin.site.register(models.SalesPackage)
admin.site.register(models.HuntingPriceList)
admin.site.register(models.HuntingPriceTypePackage)
admin.site.register(models.HuntingPackageCompanionsHunter)
admin.site.register(models.SalesPackageSpecies)
admin.site.register(models.HuntingPackageUpgradeFees)
admin.site.register(models.HuntingType)
admin.site.register(models.HuntingPriceListType)
admin.site.register(models.Currency)
# Seasons
admin.site.register(models.Seasons)
