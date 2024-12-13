from django.urls import path
from rest_framework import routers
from django.urls import include
from .views import QuotaStatsViewSets

router = routers.DefaultRouter()

router.register(r"quota-stats", QuotaStatsViewSets, basename="quotastats")


urlpatterns = [
    path("", include(router.urls)),
]
