from django.urls import path
from rest_framework import routers
from django.urls import include
from .views import (
    EntityCateriesView,
    HutingAreaViewSets,
    SpeciesListView,
    AccommodationTypeViewSets,
    PaymentMethodViewSets,
    RegulatoryHuntingPackageViewSets,
    HuntingTypesViewSets,
    CurrencyViewSets,
    SeasonsViewSets,
    DocumentTypesViewSets,
    LicenceRegulatoryHuntingPackageSpecies,
)
from .views import country_list, nationalities, contactTypes
from .other_views.priceList_views import PricesListListView, CreatePriceListViewSet

router = routers.DefaultRouter()
router.register(r"species", SpeciesListView)
router.register(r"entity-categories-vset", EntityCateriesView)
router.register(r"accommodation-types", AccommodationTypeViewSets)
# router.register(r"hunting-block", HuntingBlockView)
router.register(r"payment-methods-vset", PaymentMethodViewSets)
router.register(r"huting-areas", HutingAreaViewSets, basename="huting_areas")
router.register(
    r"regulatory-hunting-packages",
    RegulatoryHuntingPackageViewSets,
    basename="regulatory_hunting_packages",
)
router.register(r"price-list", PricesListListView)
router.register(r"create-price-list", CreatePriceListViewSet)
router.register(r"hunting-types", HuntingTypesViewSets)
router.register(r"currencies", CurrencyViewSets)
router.register(r"seasons", SeasonsViewSets)
router.register(r"document-types", DocumentTypesViewSets)
router.register(
    r"licence-regulatory-hunting-package-species",
    LicenceRegulatoryHuntingPackageSpecies,
    basename="licence_regulatory_hunting_package_species",
)


urlpatterns = [
    path("", include(router.urls)),
    path("countries/", country_list, name="country-list"),
    path("nationalities/", nationalities, name="nationalities"),
    path("contact-types/", contactTypes, name="contact_types"),
]
