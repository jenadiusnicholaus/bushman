from django.urls import path
from rest_framework import routers
from django.urls import include
from . views import SalesConfirmationViewSet
router = routers.DefaultRouter()
router.register(r'sales-confirmation-vset', SalesConfirmationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
