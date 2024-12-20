from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction

from bm_hunting_settings.models import SalesPackages
from bm_hunting_settings.other_serializers.price_list_serializers import (
    CreateSalesPackageSerializer,
    CreateSalesPackageSpeciesSerializer,
    GetSalesPackageSerializer,
)


class SalesPackageViewSet(viewsets.ModelViewSet):
    queryset = SalesPackages.objects.filter().order_by("-created_at")
    serializer_class = GetSalesPackageSerializer

    def create(self, request, *args, **kwargs):
        sales_package_data = {
            "user": request.user.id,
            "area": request.data.get("area_id"),
            "regulatory_package": request.data.get("regulatory_package_id"),
            "name": request.data.get("name"),
            "description": request.data.get("description"),
        }

        with transaction.atomic():
            sales_package_serializer = CreateSalesPackageSerializer(
                data=sales_package_data
            )
            if not sales_package_serializer.is_valid():
                return Response(
                    sales_package_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            sales_package = sales_package_serializer.save()

            species_object_list = request.data.get("species_object_list", [])

            for species_data in species_object_list:
                sales_package_species_data = {
                    "sales_package": sales_package.id,
                    "species": species_data.get("id"),
                    "quantity": species_data.get("quantity"),
                }
                sales_package_species_serializer = CreateSalesPackageSpeciesSerializer(
                    data=sales_package_species_data
                )
                if not sales_package_species_serializer.is_valid():
                    return Response(
                        sales_package_species_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                sales_package_species_serializer.save()

        return Response(
            {
                "message": "Sales package created successfully"
            },  # Fixed key-value structure
            status=status.HTTP_201_CREATED,
        )
