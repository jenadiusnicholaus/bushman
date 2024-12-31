from django.shortcuts import render

# Create your views here.
import logging

from rest_framework import viewsets

from authentication.permissions import IsAdmin
from bm_hunting_settings.models import (
    Country,
    Currency,
    GeoLocationCoordinates,
    HuntingArea,
    HuntingType,
    LocationType,
    Locations,
    Nationalities,
    QuotaHuntingAreaSpecies,
    RegulatoryHuntingPackageSpecies,
    RegulatoryHuntingpackage,
    SafaryExtras,
    SalesChartersPriceList,
    SalesPackageSpecies,
    Seasons,
    Species,
    UnitOfMeasurements,
)
from bm_hunting_settings.other_serializers.price_list_serializers import (
    GetHuntingTypeSerializer,
    GetSalesPackageSpeciesSerializer,
)
from bm_hunting_settings.serializers import (
    CountrySerializeers,
    CreateGeoLocationsSerializers,
    CreateHutingAreaSerializers,
    CreateLocationSerializer,
    CreateRegulatoryHuntingPackageSerializers,
    CreateRegulatoryHuntingPackageSpeciesSerializers,
    CreateSafaryExtrasSerializer,
    CreateSalesChartersPriceListSerializer,
    CreateSeasonsSerializer,
    EntityCategoriesSerializer,
    GetContactTypeSerializer,
    GetCurrencySerializer,
    GetDoctypeSerializer,
    GetPaymentMethodSerializer,
    GetRegulatoryHuntingPackageSerializers,
    GetRegulatoryHuntingPackageSpeciesSerializers,
    GetSafaryExtrasSerializer,
    GetSalesChartersPriceListSerializer,
    GetSeasonsSerializer,
    HutingAreaSerializers,
    NationalitiesSerializeers,
    SpeciesSerializer,
    UnitOfMeasurementsSerializer,
)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_countries import countries
from django.db import transaction

from rest_framework.decorators import api_view

from sales.models import (
    ContactType,
    Doctype,
    Entity,
    EntityCategories,
    EntityCategory,
    PaymentMethod,
    SalesInquiryPriceList,
)
from sales.serializers.sales_inquiries_serializers import GetEntitySerializers
from rest_framework import status

from sales_confirmation.models import (
    AccommodationType,
    SalesConfirmationProposalSafaryExtras,
)
from sales_confirmation.serializers import (
    CreateAccommodationTypeSerializer,
    GetAccommodationTypeSerializer,
)
from utils.handler_season_creations import SeasonCreationHandler

logger = logging.getLogger(__name__)
from django.db.models import Case, When, IntegerField


@api_view(["GET"])
def country_list(request):
    country_choices = Country.objects.all()
    serializers = CountrySerializeers(country_choices, many=True)
    return Response(serializers.data)


@api_view(["GET"])
def nationalities(request):
    country_choices = Nationalities.objects.all()
    serializers = NationalitiesSerializeers(country_choices, many=True)
    return Response(serializers.data)


@api_view(["GET"])
def contactTypes(request):
    contact_types = ContactType.objects.all()
    serializers = GetContactTypeSerializer(contact_types, many=True)

    return Response(serializers.data)


# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import Entity
# from .serializers import GetEntitySerializers


@api_view(["GET"])
def entityBySalesEquiry(request):
    sales_inquiry_id = request.query_params.get("sales_inquiry_id", None)

    if sales_inquiry_id is None:
        return Response({"error": "sales_inquiry_id is required"}, status=400)

    # Filter entities based on the provided sales_inquiry_id
    observers = Entity.objects.filter(
        sales_confirmation_proposal_observer_set__sales_inquiry__id=sales_inquiry_id
    )
    companionns = Entity.objects.filter(
        companions_set__sales_inquiry__id=sales_inquiry_id
    )
    main_hunter = Entity.objects.filter(sales_inquiry_entity_set__id=sales_inquiry_id)

    # Combine the QuerySets using the union operator
    combined_entities = (
        observers | companionns | main_hunter
    )  # Merge all three QuerySets

    # Serialize the combined results
    serializer = GetEntitySerializers(combined_entities, many=True)

    return Response(serializer.data)


class AccommodationTypeViewSets(viewsets.ModelViewSet):
    queryset = AccommodationType.objects.filter().order_by("-id")
    serializer_class = GetAccommodationTypeSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = CreateAccommodationTypeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()
        return Response(
            {
                "message": "Accommodation type created successfully",
            },
            status=status.HTTP_201_CREATED,
        )


class CurrencyViewSets(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = GetCurrencySerializer
    permission_classes = [IsAuthenticated]


class HuntingTypesViewSets(viewsets.ModelViewSet):
    queryset = HuntingType.objects.all()
    serializer_class = GetHuntingTypeSerializer
    permission_classes = [IsAuthenticated]


class UnitsViewsSet(viewsets.ModelViewSet):
    queryset = UnitOfMeasurements.objects.all()
    serializer_class = UnitOfMeasurementsSerializer
    permission_classes = [IsAuthenticated]


class PHViewSets(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = GetEntitySerializers

    def list(self, request, *args, **kwargs):
        # Filter to get the category with the name "PH"
        categories = EntityCategory.objects.filter(category__name="PH")

        # Check if any categories were found
        if not categories.exists():
            return Response(
                {"detail": "Category 'PH' not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Filter the queryset based on the retrieved categories
        queryset = self.get_queryset().filter(entity_category__in=categories)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PaymentMethodViewSets(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = GetPaymentMethodSerializer


class SeasonsViewSets(viewsets.ModelViewSet):
    serializer_class = GetSeasonsSerializer
    queryset = Seasons.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            seasons = SeasonCreationHandler.create_seasons(self, request)
        except Exception as e:
            return Response(
                {"detail": f"Error creating seasons: {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SalesChartersPriceListViewSet(viewsets.ModelViewSet):
    serializer_class = GetSalesChartersPriceListSerializer
    queryset = SalesChartersPriceList.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = {
            "name": request.data.get("name", None),
            "amount": request.data.get("amount", None),
            "currency": request.data.get("currency_id", None),
            "season": request.data.get("season_id", None),
            "description": request.data.get("description", None),
        }
        serrializers = CreateSalesChartersPriceListSerializer(data=data)
        if not serrializers.is_valid():
            return Response(serrializers.errors, status=status.HTTP_400_BAD_REQUEST)
        serrializers.save()
        return Response(
            {"message": "Price list created successfully"},
            status=status.HTTP_201_CREATED,
        )


class DocumentTypesViewSets(viewsets.ModelViewSet):
    queryset = Doctype.objects.all()
    serializer_class = GetDoctypeSerializer
    permission_classes = [IsAuthenticated]


class SpeciesListView(viewsets.ModelViewSet):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer
    # IsAdmin,
    permission_classes = [IsAuthenticated]

    def get_object(self, *args, **kwargs):
        id = self.request.query_params.get("species_id", None)
        if id is not None:
            return self.get_queryset().get(id=id)
        else:
            return None

    def list(self, request):
        area_id = self.request.query_params.get("area_id", None)

        # Get queryset while prioritizing Type 'MAIN'
        queryset = Species.objects.annotate(
            sort_order=Case(
                When(type="MAIN", then=0),  # Assign highest priority to 'MAIN'
                When(type="NORMAL", then=1),  # Assign lower priority to 'NORMAL'
                output_field=IntegerField(),
            )
        ).order_by(
            "sort_order"
        )  # Sort by the custom sort order

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=400,
            )
        serializer.save()
        return Response({"message": "Species created successfully"}, status=201)

    def patch(self, request, pk=None):
        species = self.get_object()
        serializer = self.get_serializer(species, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=400,
            )
        serializer.save()
        return Response(
            {
                "message": "Species updated successfully",
                "data": serializer.data,
            },
            status=200,
        )

    def delete(self, request, pk=None):
        species = self.get_object()
        species.delete()
        return Response(status=204)


class LicenceRegulatoryHuntingPackageSpecies(viewsets.ModelViewSet):
    serializer_class = GetRegulatoryHuntingPackageSpeciesSerializers
    queryset = RegulatoryHuntingPackageSpecies.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        quota_id = self.request.query_params.get("quota_id", None)
        querySet = self.get_queryset().filter()
        serializer = self.get_serializer(querySet, many=True)
        return Response(serializer.data)


class EntityCateriesView(viewsets.ModelViewSet):
    queryset = EntityCategories.objects.all()
    serializer_class = EntityCategoriesSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class HutingAreaViewSets(viewsets.ModelViewSet):
    serializer_class = HutingAreaSerializers
    queryset = HuntingArea.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # get all huting areas
        querySet = self.get_queryset()
        serializer = self.get_serializer(querySet, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        #  we need save
        #  1. CreateGeoLocationsSerializers
        #  2. CreateLocationSerializer
        #  3. CreateHutingAreaSerializers

        area_data = {
            "name": request.data.get("name"),
            "description": request.data.get("description"),
            "location": None,
        }

        geo_location_data = {
            "coordinates_type": request.data.get("coordinates_type"),
            # list of coordinates
            #
            # eg: "coordinates": [
            #     "lat": -6.06025,
            #     "lng": -32.76678
            # ],
            "coordinates": request.data.get("coordinates"),
        }

        location_data = {
            "location_type": request.data.get("location_type", None),
            "geo_coordinates": None,
            "is_disabled": request.data.get("is_disabled", False),
        }

        with transaction.atomic():
            geo_coordinates_serializer = CreateGeoLocationsSerializers(
                data=geo_location_data
            )

            if not geo_coordinates_serializer.is_valid():
                return Response(geo_coordinates_serializer.errors, status=400)

            saved_geo_coordinates = geo_coordinates_serializer.save()

            location_data["geo_coordinates"] = saved_geo_coordinates.id
            location_serializer = CreateLocationSerializer(data=location_data)

            if not location_serializer.is_valid():
                GeoLocationCoordinates.objects.filter(
                    id=saved_geo_coordinates.id
                ).delete()
                return Response(location_serializer.errors, status=400)

            saved_location = location_serializer.save()
            area_data["location"] = saved_location.id

            huting_area_serializer = CreateHutingAreaSerializers(data=area_data)

            if not huting_area_serializer.is_valid():
                GeoLocationCoordinates.objects.filter(
                    id=saved_geo_coordinates.id
                ).delete()
                Locations.objects.filter(id=saved_location.id).delete()

                return Response(huting_area_serializer.errors, status=400)

            saved_huting_area = huting_area_serializer.save()

            return Response(
                {"message": "Huting area created successfully"},
                status=201,
            )


class RegulatoryHuntingPackageViewSets(viewsets.ModelViewSet):
    serializer_class = GetRegulatoryHuntingPackageSerializers
    queryset = RegulatoryHuntingpackage.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # get all huting areas
        querySet = self.get_queryset()
        serializer = self.get_serializer(querySet, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        #  we save RegulatoryHuntingpackage and RegulatoryHuntingPackageSpecies

        package_data = {
            "user": request.user.id,
            "name": request.data.get("name"),
            "duration": request.data.get("duration"),
        }

        packages_species_data = {
            "species": None,
            "r_hunting_package": None,
            "quantity": None,
        }

        package_serializer = CreateRegulatoryHuntingPackageSerializers(
            data=package_data
        )

        if not package_serializer.is_valid():
            return Response(package_serializer.errors, status=400)

        package = package_serializer.save()

        for species in request.data.get("species_object_list"):
            packages_species_data["r_hunting_package"] = package.id
            packages_species_data["species"] = species.get("id")
            packages_species_data["quantity"] = species.get("quantity")

            species_serializer = CreateRegulatoryHuntingPackageSpeciesSerializers(
                data=packages_species_data
            )

            if not species_serializer.is_valid():
                RegulatoryHuntingpackage.objects.filter(id=package.id).delete()
                return Response(species_serializer.errors, status=400)

            species_serializer.save()

        return Response(
            {"message": "Package created successfully"},
            status=201,
        )


class LicenceAreaSpeciesView(viewsets.ModelViewSet):
    serializer_class = GetRegulatoryHuntingPackageSpeciesSerializers
    queryset = RegulatoryHuntingPackageSpecies.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        area_id = self.request.query_params.get("area_id", None)
        licence_id = self.request.query_params.get("licence_id", None)

        if area_id == "null" or licence_id == "null":
            return Response(
                {
                    "message": "Bad request params, Please provide area_id and licence_id"
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        if area_id is None or licence_id is None:
            return Response(
                {"message": "Bad request params,Please provide area_id and licence_id"},
                status=status.HTTP_404_NOT_FOUND,
            )

        area_species = QuotaHuntingAreaSpecies.objects.filter(
            area=area_id,
        )
        species_ids = [species.species.id for species in area_species]

        # Update lencence_species to prioritize Type 'MAIN'
        lencence_species = (
            self.get_queryset()
            .filter(
                r_hunting_package__id=licence_id,
                species__id__in=species_ids,
            )
            .annotate(
                sort_order=Case(
                    When(
                        species__type="MAIN", then=0
                    ),  # Assign highest priority to 'MAIN'
                    When(
                        species__type="NORMAL", then=1
                    ),  # Assign lower priority to 'NORMAL'
                    output_field=IntegerField(),
                )
            )
            .order_by("sort_order")
        )

        serializer = self.get_serializer(lencence_species, many=True)
        return Response(serializer.data, status=200)


class SalesPackageSpeciesView(viewsets.ModelViewSet):
    serializer_class = GetSalesPackageSpeciesSerializer
    queryset = SalesPackageSpecies.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        sales_package_id = self.request.query_params.get("sales_package_id", None)
        if sales_package_id == "null":
            return Response(
                {"message": "Bad request params, Please provide package_id"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if sales_package_id is None:
            return Response(
                {"message": "Bad request params,Please provide package_id"},
                status=status.HTTP_404_NOT_FOUND,
            )

        package_species = self.get_queryset().filter(
            sales_package__id=sales_package_id,
        )

        serializer = self.get_serializer(package_species, many=True)
        return Response(serializer.data, status=200)


class SafaryExtrasViewSets(viewsets.ModelViewSet):
    queryset = SafaryExtras.objects.filter().order_by("-created_at")
    serializer_class = GetSafaryExtrasSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # get all huting areas
        querySet = self.get_queryset()
        serializer = self.get_serializer(querySet, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = {
            "name": request.data.get("name"),
            "amount": request.data.get("amount"),
            "season": request.data.get("season_id"),
            "currency": request.data.get("currency_id"),
            "charges_per": request.data.get("charges_per"),
            "description": request.data.get("description"),
        }

        create_extras_sz = CreateSafaryExtrasSerializer(data=data)
        if not create_extras_sz.is_valid():
            return Response(create_extras_sz.errors, status=400)

        extras = create_extras_sz.save()

        return Response(
            {"message": "Safary extras created successfully"},
            status=status.HTTP_201_CREATED,
        )
