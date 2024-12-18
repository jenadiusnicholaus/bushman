from django.shortcuts import render

from approval_chain.models import ApprovalChain, ApprovalChainModule, ApprovalChainRole
from approval_chain.serializers import (
    CreateApprovalChainLevelsSerializer,
    CreateApprovalChainModuleSerializer,
    CreateApprovalChainSerializer,
    GetApprovalChainModuleSerializer,
    GetApprovalChainRoleSerializer,
    GetApprovalChainSerializer,
)
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from authentication.permissions import IsAdmin, IsValidLogin
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.shortcuts import get_object_or_404

# generic list view
from rest_framework.views import APIView


class ApprovalChainModuleViewSet(viewsets.ModelViewSet):
    serializer_class = GetApprovalChainModuleSerializer
    queryset = ApprovalChainModule.objects.all()
    permission_classes = [IsAuthenticated, IsValidLogin, IsAdmin]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        #  we need to create the followig table
        # CreateApprovalChainModuleSerializer
        # CreateApprovalChainRoleSerializer
        # CreateApprovalChainLevelsSerializer
        # CreateApprovalChainSerializer

        approval_chain_module_data = {
            "name": request.data.get("name"),
            "description": request.data.get("description"),
            "active": request.data.get("active"),
        }

        aproval_chain_objects = request.data.get("approval_chain_levels")
        if not aproval_chain_objects:
            return Response(
                {"message": "Approval chain levels are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            # approval_chain_module_serializer = CreateApprovalChainModuleSerializer(
            #     data=approval_chain_module_data
            # )
            # if not approval_chain_module_serializer.is_valid():

            #     return Response(
            #         approval_chain_module_serializer.errors,
            #         status=status.HTTP_400_BAD_REQUEST,
            #     )
            try:
                approval_chain_module, c = ApprovalChainModule.objects.get_or_create(
                    name=request.data.get("name"),
                    active=request.data.get("active"),
                    defaults={
                        "name": request.data.get("name"),
                        "description": request.data.get("description"),
                        "active": request.data.get("active"),
                    },
                )
            except Exception as e:
                return Response(
                    {
                        "message": "Error while creating approval chain module",
                        "error": str(e),
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            for aproval_chain_object in aproval_chain_objects:
                levels_data = {
                    "approval_chain_module": None,
                    "can_change_source": aproval_chain_object.get("can_change_source"),
                    "approval_chain_role": aproval_chain_object.get(
                        "approval_chain_role_id"
                    ),
                    "level_number": aproval_chain_object.get("level_number"),
                    "status": aproval_chain_object.get("status"),
                }

                approve_chain = {
                    "approval_chain_module": None,
                    "user": aproval_chain_object.get("user_id"),
                    "approval_chain_level": None,
                }

                levels_data["approval_chain_module"] = approval_chain_module.id
                levels_serializer = CreateApprovalChainLevelsSerializer(
                    data=levels_data
                )
                if not levels_serializer.is_valid():
                    #  delete the previous created data
                    approval_chain_module.delete()
                    return Response(
                        levels_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                level = levels_serializer.save()

                approve_chain["approval_chain_module"] = approval_chain_module.id
                approve_chain["approval_chain_level"] = level.id
                approve_chain_serializer = CreateApprovalChainSerializer(
                    data=approve_chain
                )
                if not approve_chain_serializer.is_valid():
                    #  delette the previous created data
                    approval_chain_module.delete()
                    level.delete()

                    return Response(
                        approve_chain_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                approve_chain_serializer.save()

        return Response(
            {"message": "Approval chain  created successfully"},
            status=status.HTTP_201_CREATED,
        )


class GetApprovalRoleApiView(APIView):
    serializer_class = GetApprovalChainRoleSerializer
    queryset = ApprovalChainRole.objects.all()
    permission_classes = [IsAuthenticated, IsValidLogin, IsAdmin]

    def get(self, request, *args, **kwargs):
        objects = ApprovalChainRole.objects.all()
        serializer = GetApprovalChainRoleSerializer(objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApprovalChainLevelsViewSet(viewsets.ModelViewSet):
    serializer_class = GetApprovalChainModuleSerializer
