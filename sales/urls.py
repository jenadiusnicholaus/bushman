from django.urls import path
from rest_framework import routers
from django.urls import include

from sales.views.sales_inquiries_views import SalesEViewViewSet
from sales.views.sales_quota_views import QuotaViewSets

router = routers.DefaultRouter()
router.register(r"sales-inquiries", SalesEViewViewSet, basename="sales_e")
router.register(r"sales-quotas", QuotaViewSets, basename="sales_quotas")


urlpatterns = [
    path("", include(router.urls)),
]
