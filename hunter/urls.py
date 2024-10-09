from django.urls import path
from rest_framework import routers
from django.urls import include

from .views.client_views import ClientViewSets, CompanionAndOberversViewSets
from .views.obervers_views import ClientObserversViewSets
from .views.companion_views import ClientCompanionsViewSets
from .views.client_docs_views import ClientDocsView


router = routers.DefaultRouter()
router.register(r"client-vset", ClientViewSets)
router.register(r"client-observer-vset", ClientObserversViewSets)
router.register(r"client-companion-vset", ClientCompanionsViewSets)
router.register(r"client-docs-vset", ClientDocsView)

router.register(
    r"companion-observer-list",
    CompanionAndOberversViewSets,
    basename="companion-observer-list",
)

urlpatterns = [
    path("", include(router.urls)),
]
