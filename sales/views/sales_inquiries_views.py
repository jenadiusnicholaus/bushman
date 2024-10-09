from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from bm_hunting_settings.serializers import CreateEntityCategorySerializer
from sales.models import Entity, EntityCategories, EntityCategory
from sales.serializers.sales_inquiries_serializers import (
    CreateEntityCategorySerializers,
    CreateEntitySerializers,
    GetEntitySerializers,
    UpdateEntitySerializers,
)
from rest_framework.response import Response
from rest_framework import status


# Create your views here.


class SalesEViewViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = GetEntitySerializers
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        entity_id = request.query_params.get("entity_id", None)
        if entity_id:
            try:
                ob = self.queryset.get(id=entity_id)
                serializer = self.get_serializer(ob)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Entity.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        entity_data = {
            "full_name": request.data.get("full_name"),
            "email": request.data.get("email"),
            "phone_number": request.data.get("phone_number"),
            "address": request.data.get("address"),
            "country": request.data.get("country"),
            "nationality": request.data.get("nationality"),
        }
        # CreateEntityCategorySerializer

        entity_serializer = CreateEntitySerializers(data=entity_data)

        if entity_serializer.is_valid():
            es = entity_serializer.save()
            entity_catory_dat = {
                "entity": es.id,
                "category": request.data.get("category"),
            }
            entity_catory_serializer = CreateEntityCategorySerializer(
                data=entity_catory_dat
            )
            if entity_catory_serializer.is_valid():
                entity_catory_serializer.save()
                return Response(
                    {
                        "message": "Entity created successfully",
                        "entity": entity_serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    entity_catory_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                entity_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def patch(self, request, *args, **kwargs):
        entity_id = request.query_params.get("entity_id", None)
        if entity_id:
            try:
                entity = Entity.objects.get(id=entity_id)
            except Entity.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            entity_data = {
                "full_name": request.data.get("full_name", entity.full_name),
                "email": request.data.get("email", entity.email),
                "phone_number": request.data.get("phone_number", entity.phone_number),
                "address": request.data.get("address", entity.address),
                "nationality": request.data.get("nationality", entity.nationality),
                "country": request.data.get("country", entity.nationality),
            }
            entity_serializer = UpdateEntitySerializers(
                entity, data=entity_data, partial=True
            )

            if entity_serializer.is_valid():
                self.perform_update(entity_serializer)
                if EntityCategory.objects.filter(entity=entity).exists():
                    c = EntityCategory.objects.filter(entity=entity).first()
                    categorySerializer = CreateEntityCategorySerializers(
                        c,
                        data={
                            "entity": entity.id,
                            "category": request.data.get("category"),
                        },
                        partial=True,
                    )
                else:
                    categorySerializer = CreateEntityCategorySerializers(
                        data={
                            "entity": entity.id,
                            "category": request.data.get("category"),
                        }
                    )
                if not categorySerializer.is_valid():
                    return Response(
                        categorySerializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
                categorySerializer.save()

                return Response(
                    {
                        "message": "Entity updated successfully",
                        "entity": entity_serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    entity_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {
                    "message": "Please provide entity_id in query params to update entity"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, *args, **kwargs):
        entity_id = request.query_params.get("entity_id", None)
        if entity_id:
            try:
                entity = Entity.objects.get(id=entity_id)
            except Entity.DoesNotExist:
                return Response(
                    {"message": "Entity does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            entity.delete()
            return Response(
                {"message": "Entity deleted successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "message": "Please provide entity_id in query params to delete entity"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
