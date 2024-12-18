from approval_chain.models import (
    ApprovalChain,
    ApprovalChainLevels,
    ApprovalChainModule,
    ApprovalChainRole,
)
from rest_framework import serializers


# -------------------- Approval Chain Module Serializer ----------
class GetApprovalChainModuleSerializer(serializers.ModelSerializer):
    approval_chain = serializers.SerializerMethodField()

    class Meta:
        model = ApprovalChainModule
        fields = "__all__"

    def get_approval_chain(self, obj):
        chains = obj.chains.all()
        serializer = GetApprovalChainSerializer(chains, many=True)
        return serializer.data


class CreateApprovalChainModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalChainModule
        fields = "__all__"


class UpdateApprovalChainModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalChainModule
        fields = "__all__"


#  -------------------- Approval Chain Role Serializer -----------------------


class GetApprovalChainRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalChainRole
        fields = "__all__"


class CreateApprovalChainRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalChainRole
        fields = "__all__"


class UpdateApprovalChainRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApprovalChainRole


# -------------------- Approval Chain Levels Serializer ----------
class GetApprovalChainLevelsSerializer(serializers.ModelSerializer):
    approval_chain_role = GetApprovalChainRoleSerializer()

    class Meta:
        model = ApprovalChainLevels
        fields = "__all__"


class CreateApprovalChainLevelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalChainLevels
        fields = "__all__"


class UpdateApprovalChainLevelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalChainLevels


# -------------------- Approval Chain Level Serializer ----------
class GetApprovalChainSerializer(serializers.ModelSerializer):
    approval_chain_level = GetApprovalChainLevelsSerializer()

    class Meta:
        model = ApprovalChain
        fields = "__all__"


class CreateApprovalChainSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalChain
        fields = "__all__"


class UpdateApprovalChainSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalChain
        fields = "__all__"
