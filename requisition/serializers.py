from rest_framework import serializers

from approval_chain.models import ApprovalChainModule
from approval_chain.serializers import GetApprovalChainLevelsSerializer
from authentication.serialisers.profile_serializers import GetUserSerializer
from requisition.models import (
    RemarksHistory,
    RequestItem,
    RequestItemAccount,
    RequestItemItems,
    RequestItemSource,
    Requisition,
)


# --------------------- Serializers ----------
class GetRequisitionSerializer(serializers.ModelSerializer):
    level = GetApprovalChainLevelsSerializer()
    next_level = serializers.SerializerMethodField()
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
            next_level = approval_chain.levels.filter(
                level_number__gt=obj.level.level_number
            )
            if not next_level.exists():

                return None

            next_level = next_level.first()
            serializer = GetApprovalChainLevelsSerializer(next_level)
            return serializer.data
        except ApprovalChainModule.DoesNotExist:
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
