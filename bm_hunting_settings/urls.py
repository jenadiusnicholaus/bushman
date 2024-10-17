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
)
from .views import country_list, nationalities, contactTypes
from .other_views.priceList_views import PriceListViewSet

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
router.register(r"price-list", PriceListViewSet, basename="sales_packages")


urlpatterns = [
    path("", include(router.urls)),
    path("countries/", country_list, name="country-list"),
    path("nationalities/", nationalities, name="nationalities"),
    path("contact-types/", contactTypes, name="contact_types"),
]
