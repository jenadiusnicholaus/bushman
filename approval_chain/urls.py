from django.urls import path
from rest_framework import routers
from django.urls import include
from .views import (
    ApprovalChainLevelsVset,
    ApprovalChainModuleViewSet,
    GetApprovalRoleApiView,
)

router = routers.DefaultRouter()

router.register(
    r"approval-chain-vset",
    ApprovalChainModuleViewSet,
    basename="approval_chain_module",
)

router.register(
    r"approval-chain-levels-vset",
    ApprovalChainLevelsVset,
    basename="approval-chain-levels",
)


urlpatterns = [
    path("", include(router.urls)),
    path(
        "approval-chain-role/",
        GetApprovalRoleApiView.as_view(),
        name="get_approval_role",
    ),
]
