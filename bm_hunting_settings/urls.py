from django.urls import path
from rest_framework import routers
from django.urls import include
from .views import EntityCateriesView, SpeciesListView, HuntingBlockView
from .views import country_list

router = routers.DefaultRouter()
router.register(r"species", SpeciesListView)
router.register(r"entity-categories-vset", EntityCateriesView)
router.register(r"hunting-block", HuntingBlockView)


urlpatterns = [
    path("", include(router.urls)),
    path("countries/", country_list, name="country-list"),
]
