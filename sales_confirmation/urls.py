from django.urls import path
from rest_framework import routers
from django.urls import include
from .views import (
    SalesConfirmationViewSet,
    CalculateTotalSalesAmount,
    SalesConfirmation,
    GetCalendaStats,
)

router = routers.DefaultRouter()
router.register(r"sales-confirmation-vset", SalesConfirmationViewSet)
router.register(
    r"sales-confirmation-status-vset", SalesConfirmation, basename="sales-confirmation"

)
router.register(r"calendar-stats-vset", GetCalendaStats, basename="calendar-stats")

urlpatterns = [
    path("", include(router.urls)),
    path("sales-price-break-down/", CalculateTotalSalesAmount.as_view()),
]
