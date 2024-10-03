from django.shortcuts import render

# Create your views here.
import logging

from rest_framework import  viewsets

from authentication.permissions import IsAdmin
from bm_hunting_settings.models import Species
from hunter.serializers.hunting_setting_sz import SpeciesSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class SpeciesListView(viewsets.ModelViewSet):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer
    permission_classes = [IsAdmin,IsAuthenticated]

    def get_object(self, *args, **kwargs):
        id = self.request.query_params.get('species_id', None)
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
    