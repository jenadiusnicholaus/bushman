from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from ..other_serializers.price_list_serializers import (
    CreateHuntingPackageCompanionsHunterSerializer,
    CreateHuntingPriceTypePackageSerializer,
    CreateSalesPackageSerializer,
    CreateHuntingPriceListSerializer,
    CreateHuntingPriceListTypeSerializer,
    GetHuntingPriceListSerializer,
    GetHuntingPriceTypePackageSerializer,
    CreateSalesPackageSpeciesSerializer,
    GetSalesPackageSerializer,
)

from ..models import (
    SalesPackages,
    HuntingPriceList,
    HuntingPriceListType,
    HuntingPriceTypePackage,
    SalesPackageSpecies,
)

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from pprint import pprint
from datetime import datetime

current_year = datetime.now().year


class CreatePriceListViewSet(viewsets.ModelViewSet):
    serializer_class = GetHuntingPriceListSerializer

    queryset = HuntingPriceList.objects.filter(
        hunting_price_list_type__hunting_price_type_package__sales_package__sales_quota__start_date__year=current_year
    )
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        pprint(request.data)

        sales_package_data = {
            "user": request.user.id,
            "name": request.data.get("name"),
            "description": request.data.get("description"),
            "sales_quota": request.data.get("sales_quota_id"),
        }
        price_list_data = {
            "area": request.data.get("area"),
            "user": request.user.id,
            "start_date": request.data.get("start_date", None),
            "end_date": request.data.get("end_date", None),
        }
        price_list_type_data = {
            "amount": request.data.get("amount"),
            "currency": request.data.get("currency"),
            "hunting_type": request.data.get("hunting_type_id"),
            "duration": request.data.get("duration"),
        }

        sales_package = None
        price_list = None
        price_list_type = None

        with transaction.atomic():
            # Create the Sales Package
            sales_package_serializer = CreateSalesPackageSerializer(
                data=sales_package_data
            )
            if not sales_package_serializer.is_valid():
                return Response(
                    sales_package_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
            sales_package = sales_package_serializer.save()

            # Create the Hunting Price List
            price_list_data["sales_package"] = sales_package.id
            price_list_serializer = CreateHuntingPriceListSerializer(
                data=price_list_data
            )
            if not price_list_serializer.is_valid():
                sales_package.delete()  # Delete the previously created sales_package
                return Response(
                    price_list_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            price_list = price_list_serializer.save()

            # Create the Hunting Price List Type
            price_list_type_data["price_list"] = price_list.id
            price_list_type_serializer = CreateHuntingPriceListTypeSerializer(
                data=price_list_type_data
            )
            if not price_list_type_serializer.is_valid():

                price_list.delete()  # Delete the previously created price_list
                sales_package.delete()  # Delete the previously created sales_package
                return Response(
                    price_list_type_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            price_list_type = price_list_type_serializer.save()

            # Create the Hunting Price Type Package
            hunting_price_type_package_data = {
                "price_list_type": price_list_type.id,
                "sales_package": sales_package.id,
            }
            hunting_price_type_package_serializer = (
                CreateHuntingPriceTypePackageSerializer(
                    data=hunting_price_type_package_data
                )
            )

            if not hunting_price_type_package_serializer.is_valid():
                price_list_type.delete()  # Delete the previously created price_list_type
                price_list.delete()  # Delete the previously created price_list
                sales_package.delete()  # Delete the previously created sales_package
                return Response(
                    hunting_price_type_package_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            saved_hunting_price_type_package = (
                hunting_price_type_package_serializer.save()
            )

            # GetHuntingPackageCompanionsHunterSerializer
            componants_hunter_data = {
                "hunting_price_list_type_package": saved_hunting_price_type_package.id,
                "days": request.data.get("companion_days"),
                "amount": request.data.get("companion_amount"),
            }
            componion_hunter_serializer = (
                CreateHuntingPackageCompanionsHunterSerializer(
                    data=componants_hunter_data
                )
            )
            pprint(componion_hunter_serializer.is_valid())
            if not componion_hunter_serializer.is_valid():
                # Clean up the previously created objects for data consistency
                hunting_price_type_package_serializer.save()  # Assuming this can be re-saved or skip deletion
                price_list_type.delete()  # Delete the previously created price_list_type
                price_list.delete()  # Delete the previously created price_list
                sales_package.delete()  # Delete the previously created sales_package
                return Response(
                    componion_hunter_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            componion_hunter_serializer.save()

            # Create Sales Package Species Data
            species_object_list = request.data.get("species_object_list", [])

            pprint(species_object_list.__len__())
            for species_data in species_object_list:
                sales_package_species_data = {
                    "sales_package": sales_package.id,
                    "species": species_data.get("id"),
                    "quantity": species_data.get("quantity"),
                    "amount": species_data.get("amount"),
                }
                sales_package_species_serializer = CreateSalesPackageSpeciesSerializer(
                    data=sales_package_species_data
                )
                pprint(sales_package_species_serializer.is_valid())
                if not sales_package_species_serializer.is_valid():
                    # Clean up the previously created objects
                    hunting_price_type_package_serializer.save()  # Assuming this can be re-saved or skip deletion
                    price_list_type.delete()  # Delete the previously created price_list_type
                    price_list.delete()  # Delete the previously created price_list
                    sales_package.delete()  # Delete the previously created sales_package
                    return Response(
                        sales_package_species_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                sales_package_species_serializer.save()

        return Response(
            {
                "message": "Price List created successfully",
            },
            status=status.HTTP_201_CREATED,
        )


class PricesListListView(viewsets.ModelViewSet):
    serializer_class = GetHuntingPriceTypePackageSerializer
    queryset = HuntingPriceTypePackage.objects.all().order_by("-create_date")
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            self.queryset
        )  # No need for a separate filter, just return the base queryset

    def list(self, request, *args, **kwargs):
        # Retrieve query parameters; default to None if they are not present
        hunting_type_id = request.query_params.get("hunting_type_id")
        area_id = request.query_params.get("area_id")
        quota_id = request.query_params.get("quota_id")  # sales_quota_id

        # Start with the base queryset
        queryset = self.get_queryset()

        filters = {}

        # Only add filters for parameters that are not None or empty
        if hunting_type_id not in (None, ""):
            filters["price_list_type__hunting_type__id"] = hunting_type_id
        if area_id not in (None, ""):
            filters["price_list_type__price_list__area__id"] = area_id
        if quota_id not in (None, ""):
            filters["sales_package__sales_quota__id"] = quota_id

        # Apply filters to the queryset if any filter has been added
        if filters:
            queryset = queryset.filter(**filters)

        # Always order by create_date in descending order
        queryset = queryset.order_by("-create_date")

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

        # queryset = self.get_queryset().order_by("-create_date")
        # serializer = self.get_serializer(queryset, many=True)
        # return Response(serializer.data)
