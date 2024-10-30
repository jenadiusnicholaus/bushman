from rest_framework import viewsets

from bm_hunting_settings.models import HuntingPackageCustomization
from bm_hunting_settings.other_serializers.package_customization import (
    CreateCustomizedPackageSerializer,
    CreateCustomizedSpeciesSerializer,
    GetCustomzedPackageSerializer,
)
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status


class PackageCustomizationView(viewsets.ModelViewSet):
    queryset = HuntingPackageCustomization.objects.all()
    serializer_class = GetCustomzedPackageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Create customization data
        customization_data = {
            "hunting_price_list_type_package": request.data.get("package_id"),
            "amount": request.data.get("amount"),
            "hunting_type": request.data.get("hunting_type_id"),
            "area": request.data.get("area_id"),
            "season": request.data.get("season_id"),
        }

        species_list_dict = request.data.get("species_list", [])

        with transaction.atomic():
            # Validate and save the customized package
            customized_serializer = CreateCustomizedPackageSerializer(
                data=customization_data
            )
            if not customized_serializer.is_valid():
                return Response(
                    customized_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
            customized_package = customized_serializer.save()

            for species_dict in species_list_dict:
                species_data = {
                    "species": species_dict.get("species_id"),
                    "hunting_package_customization": customized_package.id,
                    "amount": species_dict.get("amount"),
                    "quantity": species_dict.get("quantity"),  # Corrected spelling
                }
                species_serializer = CreateCustomizedSpeciesSerializer(
                    data=species_data
                )

                if not species_serializer.is_valid():
                    transaction.set_rollback(True)
                    return Response(
                        species_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

                species_serializer.save()

            return Response(customized_serializer.data, status=status.HTTP_201_CREATED)
