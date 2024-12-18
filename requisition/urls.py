from django.urls import path
from rest_framework import routers
from django.urls import include
from .views import RequisitionVewSet, RequisitionItemViewSet

router = routers.DefaultRouter()
router.register(r"requisition-vset", RequisitionVewSet, basename="requisition")
router.register(
    r"requisition-item-vset", RequisitionItemViewSet, basename="requisition-item"
)

urlpatterns = [
    path("", include(router.urls)),
]
