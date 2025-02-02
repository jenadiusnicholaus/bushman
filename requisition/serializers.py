from rest_framework import serializers

from approval_chain.models import ApprovalChainModule
from approval_chain.serializers import GetApprovalChainLevelsSerializer
from authentication.serialisers.profile_serializers import GetUserSerializer
from bm_hunting_settings.models import UnitOfMeasurements
from bm_hunting_settings.serializers import (
    GetCurrencySerializer,
    UnitOfMeasurementsSerializer,
)
from requisition.models import (
    RemarksHistory,
    RequestItem,
    RequestItemAccount,
    RequestItemItems,
    RequestItemSource,
    Requisition,
    RequisitionApprovalStatus,
)


# --------------------- Serializers ----------
class GetRequisitionSerializer(serializers.ModelSerializer):
    level = GetApprovalChainLevelsSerializer()
    next_level = serializers.SerializerMethodField()
    current_level_status = serializers.SerializerMethodField()
    requested_by = GetUserSerializer()
    type = serializers.CharField(source="get_type_display")

    def get_next_level(self, obj):
        # get the next level of the approval chain
        if obj.status == "APPROVED" or obj.status == "REJECTED":
            return None
        try:

            approval_chain = ApprovalChainModule.objects.get(
                id=obj.approval_chain_module.id
            )
            status = RequisitionApprovalStatus.objects.get(
                requisition=obj,
            )

            levels = approval_chain.levels.all()
            # get all levels not yet in status and  fins the next level
            next_level = levels.exclude(id__in=[status.level.id])
            excluded_ids = next_level.values_list("id", flat=True)

            _next_level = next_level.first()
            serializer = GetApprovalChainLevelsSerializer(_next_level)
            return serializer.data
        except ApprovalChainModule.DoesNotExist:
            return None

    def get_current_level_status(self, obj):
        # get the current level status of the requisition
        # GetRequisitionApprovalStatusSerializer
        try:
            level_status = RequisitionApprovalStatus.objects.get(
                requisition=obj, level=obj.level
            )
            serializer = GetRequisitionApprovalStatusSerializer(level_status)
            return serializer.data
        except RequisitionApprovalStatus.DoesNotExist:
            return None

    class Meta:
        model = Requisition
        fields = "__all__"


class CreateRequisitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requisition
        fields = "__all__"


class UpdateRequisitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requisition
        fields = "__all__"


# ---------- Serializers for RequestItemSource ----------
class GetRequestItemSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestItemSource
        fields = "__all__"


class CreateRequestItemSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestItemSource
        fields = "__all__"


class UpdateRequestItemSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestItemSource
        fiels = "__all__"


# ---------- End of Serializers for RequestItemSource ----------
class GetRequestItemSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    accounts = serializers.SerializerMethodField()

    def get_accounts(self, obj):
        try:
            accounts = RequestItemAccount.objects.get(requisition_item=obj)
        except RequestItemAccount.DoesNotExist:
            return None
        serializer = GetRequestItemAccountsSerializer(accounts)
        return serializer.data

    def get_items(self, obj):
        items = obj.item_items_set.all()
        serializer = GetRequestItemItemsSerializer(items, many=True)
        return serializer.data

    class Meta:
        model = RequestItem
        fields = "__all__"


class CreateRequestItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestItem
        fields = "__all__"


class UpdateRequestItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestItem
        fields = "__all__"


# ---------- End of Serializers for RequestItem ----------
class GetRequestItemItemsSerializer(serializers.ModelSerializer):
    unit_of_measurement = serializers.SerializerMethodField()
    currency = GetCurrencySerializer()

    def get_unit_of_measurement(self, obj):
        try:
            unit_of_measurement = UnitOfMeasurements.objects.get(
                id=obj.unit_of_measurement.id
            )
        except UnitOfMeasurements.DoesNotExist:
            return None
        serializer = UnitOfMeasurementsSerializer(unit_of_measurement)
        return serializer.data

    class Meta:
        model = RequestItemItems
        fields = "__all__"


class CreateRequestItemItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestItemItems
        fields = "__all__"


class UpdateRequestItemItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestItemItems
        fields = "__all__"


class GetRequestItemAccountsSerializer(serializers.ModelSerializer):
    currency = GetCurrencySerializer()

    class Meta:
        model = RequestItemAccount
        fields = "__all__"


class CreateRequestItemAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestItemAccount
        fields = "__all__"


class UpdateRequestItemAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestItemAccount
        fields = "__all__"


# remarks history serializer
class GetRemarksHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RemarksHistory
        fields = "__all__"


class CreateRemarksHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RemarksHistory
        fields = "__all__"


class UpdateRemarksHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RemarksHistory
        fields = "__all__"


class GetRequisitionApprovalStatusSerializer(serializers.ModelSerializer):
    level = GetApprovalChainLevelsSerializer()

    class Meta:
        model = RequisitionApprovalStatus
        fields = "__all__"


class CreateRequisitionApprovalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequisitionApprovalStatus
        fields = "__all__"


class UpdateRequisitionApprovalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequisitionApprovalStatus
        fields = "__all__"
