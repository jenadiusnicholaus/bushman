from django.urls import path
from rest_framework import routers
from django.urls import include
from .views import (
    SalesConfirmationViewSet,
    CalculateTotalSalesAmount,
    SalesConfirmation,
    GetCalendaStats,
)

from .other_views.sales_conf_contract_views import (
    InitiateClientGameViewSet,
    SalesConfirmationContractviewSet,
    EntityContractPermitViewset,
    ClientGameActivityViewset,
    GameActivityRegistrationForWebPlatFormvieSet,
    GameActivitiesViewSet,
)
from .other_views.companion_observer_views import (
    SalesConfirmationCompanionViewSets,
    SalesConfirmationProposalObserversViewSets,
)

router = routers.DefaultRouter()
router.register(r"sales-confirmation-vset", SalesConfirmationViewSet)
router.register(
    r"sales-confirmation-status-vset", SalesConfirmation, basename="sales-confirmation"
)
router.register(r"calendar-stats-vset", GetCalendaStats, basename="calendar-stats")
router.register(
    r"sales-confirmation-contract-vset",
    SalesConfirmationContractviewSet,
    basename="sales-confirmation-contract",
)
router.register(
    r"entity-contract-permit-vset",
    EntityContractPermitViewset,
    basename="entity-contract-permit",
)

router.register(
    r"game-activity-vset",
    ClientGameActivityViewset,
)
router.register(
    r"game-activity-registration-vset",
    GameActivityRegistrationForWebPlatFormvieSet,
    basename="game-activity-registration-for-web-plat-form",
)

router.register(
    r"game-activities-vset",
    GameActivitiesViewSet,
    basename="game-activities",
)
router.register(
    r"sales-confirmation-companion-vset",
    SalesConfirmationCompanionViewSets,
    basename="sales-confirmation-companion",
)

router.register(
    r"sales-confirmation-proposal-observers-vset",
    SalesConfirmationProposalObserversViewSets,
    basename="sales-confirmation-proposal-observers",
)

urlpatterns = [
    path("", include(router.urls)),
    path("sales-price-break-down/", CalculateTotalSalesAmount.as_view()),
    path("create-game-activity-vset/", InitiateClientGameViewSet.as_view()),
]
