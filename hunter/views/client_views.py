from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from authentication.serialisers.profile_serializers import (
    CreateUserProfileSerializer,
    CreateUserSerializer,
)
from hunter.models import Client, Observer
from hunter.serializers.client_sz import (
    GetClientSerializer,
    GetOberverAndCompanionSerializer,
)
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.auth.models import User

from hunter.serializers.observer_sz import (
    CreateObserverClientSerializer,
    GetObserverClientSerializer,
)


class ClientViewSets(viewsets.ModelViewSet):
    serializer_class = GetClientSerializer
    queryset = Client.objects.all()
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CompanionAndOberversViewSets(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    permission_classes = [AllowAny]
    serializer_class = GetOberverAndCompanionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.get(user__id=request.user.id)
        serializer = GetOberverAndCompanionSerializer(queryset)
        return Response(serializer.data)
