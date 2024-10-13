from django.shortcuts import render

# Create your views here.
import logging

from rest_framework import viewsets

from authentication.permissions import IsAdmin
from bm_hunting_settings.models import (
    AccommodationType,
    Country,
    HuntingArea,
    Nationalities,
    QuotaHutingAreaSpecies,
    Species,
)
from bm_hunting_settings.serializers import (
    CountrySerializeers,
    EntityCategoriesSerializer,
    GetAccommodationTypeSerializer,
    GetContactTypeSerializer,
    GetPaymentMethodSerializer,
    HutingAreaSerializers,
    NationalitiesSerializeers,
    SpeciesSerializer,
)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_countries import countries

from rest_framework.decorators import api_view

from sales.models import ContactType, EntityCategories, PaymentMethod

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


class PaymentMethodViewSets(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = GetPaymentMethodSerializer


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
        queryset = Species.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, pk=None):
        species = self.get_object()
        serializer = self.get_serializer(species, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

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
