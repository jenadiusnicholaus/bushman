
from django.urls import path
from rest_framework import routers  
from django.urls import include
from . views import   SpeciesListView

router = routers.DefaultRouter()
router.register('species', SpeciesListView)

urlpatterns = [
    path('', include(router.urls)),
]