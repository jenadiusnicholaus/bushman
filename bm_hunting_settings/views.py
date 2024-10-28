from django.shortcuts import render

# Create your views here.
import logging

from rest_framework import viewsets

from authentication.permissions import IsAdmin
from bm_hunting_settings.models import (
    AccommodationType,
    Country,
    Currency,
    GeoLocationCoordinates,
    HuntingArea,
    HuntingType,
    LocationType,
    Locations,
    Nationalities,
    QuotaHutingAreaSpecies,
    RegulatoryHuntingpackage,
    Seasons,
    Species,
)
from bm_hunting_settings.other_serializers.price_list_serializers import (
    GetHuntingTypeSerializer,
)
from bm_hunting_settings.serializers import (
    CountrySerializeers,
    CreateGeoLocationsSerializers,
    CreateHutingAreaSerializers,
    CreateLocationSerializer,
    CreateRegulatoryHuntingPackageSerializers,
    CreateRegulatoryHuntingPackageSpeciesSerializers,
    EntityCategoriesSerializer,
    GetAccommodationTypeSerializer,
    GetContactTypeSerializer,
    GetCurrencySerializer,
    GetDoctypeSerializer,
    GetPaymentMethodSerializer,
    GetRegulatoryHuntingPackageSerializers,
    GetSeasonsSerializer,
    HutingAreaSerializers,
    NationalitiesSerializeers,
    SpeciesSerializer,
)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_countries import countries
from django.db import transaction

from rest_framework.decorators import api_view

from sales.models import ContactType, Doctype, EntityCategories, PaymentMethod

logger = logging.getLogger(__name__)


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


class AccommodationTypeViewSets(viewsets.ModelViewSet):
    queryset = AccommodationType.objects.all()
    serializer_class = GetAccommodationTypeSerializer
    permission_classes = [IsAuthenticated]


class CurrencyViewSets(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = GetCurrencySerializer
    permission_classes = [IsAuthenticated]


class HuntingTypesViewSets(viewsets.ModelViewSet):
    queryset = HuntingType.objects.all()
    serializer_class = GetHuntingTypeSerializer
    permission_classes = [IsAuthenticated]


class PaymentMethodViewSets(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = GetPaymentMethodSerializer


class SeasonsViewSets(viewsets.ModelViewSet):
    serializer_class = GetSeasonsSerializer
    queryset = Seasons.objects.all()
    permission_classes = [IsAuthenticated]

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
        queryset = Species.objects.all()
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
            "quota": request.data.get("quota_id"),
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
