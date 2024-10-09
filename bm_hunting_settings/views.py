from django.shortcuts import render

# Create your views here.
import logging

from rest_framework import viewsets

from authentication.permissions import IsAdmin
from bm_hunting_settings.models import HuntingBlock, Species
from bm_hunting_settings.serializers import (
    EntityCategoriesSerializer,
    GetHuntingBlockSerializer,
    SpeciesSerializer,
)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_countries import countries

from rest_framework.decorators import api_view

from sales.models import EntityCategories

logger = logging.getLogger(__name__)


@api_view(["GET"])
def country_list(request):
    country_choices = [{"code": code, "name": name} for code, name in countries]
    return Response(country_choices)


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


class HuntingBlockView(viewsets.ModelViewSet):
    queryset = HuntingBlock.objects.all()
    serializer_class = GetHuntingBlockSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        countries_list = list(countries)
        return Response(countries_list)
