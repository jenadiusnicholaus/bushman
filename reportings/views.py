from django.shortcuts import render
from rest_framework import viewsets

from bm_hunting_settings.models import Quota
from .serializers import GetQuotaStatsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


# Create your views here.


class QuotaStatsViewSets(viewsets.ModelViewSet):

    queryset = Quota.objects.filter()
    serializer_class = GetQuotaStatsSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        from utils.utitlities import CurrentQuota

        current_quota = CurrentQuota.current_quota
        queryset = self.get_queryset().filter(id=current_quota.id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
