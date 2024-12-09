from django.urls import path
from rest_framework import routers
from django.urls import include

from sales.views.sales_inquiries_views import (
    SalesInquiriesClientBasicinfosViewSet,
    SalesInquiriesViewSet,
    SalesClientContactsViewSet,
    SalesIquiryPreferenceViewSet,
    SearchSalesInquiriesViewSet,
)
from sales.views.sales_quota_views import (
    QuotaViewSets,
    QuotaHuntingAreaSpeciesViewSets,
)

router = routers.DefaultRouter()
router.register(
    r"sales-inquiries-basic-infos",
    SalesInquiriesClientBasicinfosViewSet,
    basename="sales_inquiries_basic_infos",
)
router.register(r"sales-inquiries", SalesInquiriesViewSet, basename="sales_inquiries")
router.register(r"sales-quotas", QuotaViewSets, basename="sales_quotas")
router.register(
    r"sales-client-contacts",
    SalesClientContactsViewSet,
    basename="sales_client_contacts",
)
router.register(
    r"sales-inquiry-preferences",
    SalesIquiryPreferenceViewSet,
    basename="sales_inquiry_preferences",
)
router.register(
    r"sales-quotas-hunting-area-species-vset",
    QuotaHuntingAreaSpeciesViewSets,
    basename="sales_quotas_huting_area_species",
)

router.register(
    r"search-sales-inquiries",
    SearchSalesInquiriesViewSet,
    basename="search_sales_inquiries",
)


urlpatterns = [
    path("", include(router.urls)),
]
