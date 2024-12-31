from rest_framework import viewsets

from bm_hunting_settings.models import IdentityType
from sales.helpers import SalesHelper
from sales.models import Entity, EntityCategories
from sales.serializers.sales_inquiries_serializers import (
    CreateEntityCategorySerializers,
    CreateEntityIdentitySerializers,
    CreateEntitySerializers,
)
from sales_confirmation.models import (
    SalesConfirmationCompanions,
    SalesConfirmationProposalObserver,
)
from sales_confirmation.serializers import (
    CreateSalesConfirmationCompanionsSerializer,
    CreateSalesConfirmationProposalObserverSerializer,
    GetSalesConfirmationCompanionsSerializer,
    GetSalesConfirmationProposalObserverSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from rest_framework.permissions import IsAuthenticated


class SalesConfirmationCompanionViewSets(viewsets.ModelViewSet):
    queryset = SalesConfirmationCompanions.objects.all()
    serializer_class = GetSalesConfirmationCompanionsSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        sales_inquiry_id = self.request.query_params.get("sales_inquiry_id", None)
        enity_id = self.request.query_params.get("entity_id", None)
        if sales_inquiry_id is not None:
            queryset = queryset.filter(
                sales_inquiry__id=sales_inquiry_id,
                # companion__id=enity_id,
            )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        identity, _ = IdentityType.objects.get_or_create(name="passport_number")
        categories, _ = EntityCategories.objects.get_or_create(name="companion_hunter")

        entity_data = {
            "user": request.user.id,
            "full_name": request.data.get("full_name"),
            "nationality": request.data.get("nationality_id"),
            "country": request.data.get("country_id"),
        }

        companion_data = {
            "sales_inquiry": request.data.get("sales_inquiry_id"),
            "companion": None,
            "charter_in": request.data.get("charter_in"),
            "charter_out": request.data.get("charter_out"),
            "regulatory_package": request.data.get("regulatory_package_id"),
            "arrival_airport": request.data.get("arrival_airport"),
        }

        with transaction.atomic():
            entity_serializer = CreateEntitySerializers(data=entity_data)
            if not entity_serializer.is_valid():
                return Response(
                    entity_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            saved_entity = entity_serializer.save()

            entity_identity_data = {
                "entity": saved_entity.id,
                "identity_type": identity.id,
                "identity_number": request.data.get("identity_number"),
            }
            entity_identity_serializer = CreateEntityIdentitySerializers(
                data=entity_identity_data
            )
            if not entity_identity_serializer.is_valid():
                saved_entity.delete()
                return Response(
                    entity_identity_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            saved_identity = entity_identity_serializer.save()

            category_data = {
                "entity": saved_entity.id,
                "category": categories.id,
            }
            entity_category_serializer = CreateEntityCategorySerializers(
                data=category_data
            )
            if not entity_category_serializer.is_valid():
                saved_entity.delete()
                saved_identity.delete()
                return Response(
                    entity_category_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            saved_category_serializer = entity_category_serializer.save()

            try:
                SalesHelper.save_contacts(
                    contacts=request.data.get("contacts"),
                    contact_request_data={
                        "entity": saved_entity.id,
                        "contact_type": None,
                        "contact": None,
                    },
                    saved_entity_serializer=saved_entity,
                    category_serializer=saved_category_serializer,
                )
            except Exception as e:

                return Response(
                    {"message": "Error while saving contacts", "error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            companion_data.update({"companion": saved_entity.id})
            companion_serializer = CreateSalesConfirmationCompanionsSerializer(
                data=companion_data
            )
            if not companion_serializer.is_valid():
                saved_entity.delete()
                saved_identity.delete()
                saved_category_serializer.delete()
                return Response(
                    companion_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            saved_companion = companion_serializer.save()

            return Response(
                {"message": "Companion created successfully"},
                status=status.HTTP_201_CREATED,
            )


class SalesConfirmationProposalObserversViewSets(viewsets.ModelViewSet):
    queryset = SalesConfirmationProposalObserver.objects.all()
    serializer_class = GetSalesConfirmationProposalObserverSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        sales_inquiry_id = self.request.query_params.get("sales_inquiry_id", None)
        entity_id = self.request.query_params.get("entity_id", None)
        if sales_inquiry_id is not None:
            queryset = queryset.filter(
                sales_inquiry__id=sales_inquiry_id,
                # observer=entity_id,
            )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        identity, _ = IdentityType.objects.get_or_create(name="passport_number")
        categories, _ = EntityCategories.objects.get_or_create(name="observer")

        entity_data = {
            "user": request.user.id,
            "full_name": request.data.get("full_name"),
            "nationality": request.data.get("nationality_id"),
            "country": request.data.get("country_id"),
        }
        observer_data = {
            "sales_inquiry": request.data.get("sales_inquiry_id"),
            "observer": None,
            "charter_in": request.data.get("charter_in"),
            "charter_out": request.data.get("charter_out"),
            "arrival_airport": request.data.get("arrival_airport"),
        }

        with transaction.atomic():
            entity_serializer = CreateEntitySerializers(data=entity_data)
            if not entity_serializer.is_valid():
                return Response(
                    entity_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            saved_entity = entity_serializer.save()

            entity_identity_data = {
                "entity": saved_entity.id,
                "identity_type": identity.id,
                "identity_number": request.data.get("identity_number"),
            }
            entity_identity_serializer = CreateEntityIdentitySerializers(
                data=entity_identity_data
            )
            if not entity_identity_serializer.is_valid():
                saved_entity.delete()
                return Response(
                    entity_identity_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            saved_identity = entity_identity_serializer.save()

            category_data = {
                "entity": saved_entity.id,
                "category": categories.id,
            }
            entity_category_serializer = CreateEntityCategorySerializers(
                data=category_data
            )
            if not entity_category_serializer.is_valid():
                saved_entity.delete()
                saved_identity.delete()
                return Response(
                    entity_category_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            saved_category_serializer = entity_category_serializer.save()

            try:
                SalesHelper.save_contacts(
                    contacts=request.data.get("contacts"),
                    contact_request_data={
                        "entity": saved_entity.id,
                        "contact_type": None,
                        "contact": None,
                    },
                    saved_entity_serializer=saved_entity,
                    category_serializer=saved_category_serializer,
                )
            except Exception as e:
                return Response(
                    {"message": "Error while saving contacts", "error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            observer_data.update({"observer": saved_entity.id})
            observer_serializer = CreateSalesConfirmationProposalObserverSerializer(
                data=observer_data
            )
            if not observer_serializer.is_valid():
                saved_entity.delete()
                saved_identity.delete()
                saved_category_serializer.delete()
                return Response(
                    observer_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            saved_observer = observer_serializer.save()

            return Response(
                {"message": "Observer created successfully"},
                status=status.HTTP_201_CREATED,
            )
