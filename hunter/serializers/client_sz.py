from rest_framework import serializers

from authentication.serialisers.profile_serializers import (
    GetProfileSerializer,
    GetUserSerializer,
)
from hunter.serializers.companion_sz import GetCompanionClientSerializer
from hunter.serializers.observer_sz import GetObserverClientSerializer
from ..models import Client, Companion, Observer


class GetClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"
        depth = 2


class CreateClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = "__all__"


class GetOberverAndCompanionSerializer(serializers.ModelSerializer):
    observer_and_companion = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ["observer_and_companion"]

    def get_observer_and_companion(self, obj):
        observer_and_companion = []
        try:
            # user = self.context["request"].user
            observer = Observer.objects.filter(client=obj)
            observer_serializer = GetObserverClientSerializer(observer, many=True)
            companion = Companion.objects.filter(client=obj)
            companion_serializer = GetCompanionClientSerializer(companion, many=True)
            #  combaine two obj listo  to one

            observer_and_companion.extend(observer_serializer.data)
            observer_and_companion.extend(companion_serializer.data)
        except:
            observer_and_companion = []
        return observer_and_companion
