from django.shortcuts import render
from rest_framework import viewsets

from bm_hunting_settings.models import Quota
from utils.utitlities import currentQuuta
from .serializers import GetQuotaStatsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


# Create your views here.

current_quota = currentQuuta.current_quota


class QuotaStatsViewSets(viewsets.ModelViewSet):
    queryset = Quota.objects.filter(id=current_quota.id)
    serializer_class = GetQuotaStatsSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
