from rest_framework import serializers

from bm_hunting_settings.models import HuntingBlock, HuntingBlockSpeciesLimit, Species


class GetHuntingBlockSpeciesLimitSpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuntingBlockSpeciesLimit
        fields = "__all__"


class CreateHuntingBlockSpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuntingBlockSpeciesLimit
        fields = "__all__"


class UpdateHuntingBlockSpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuntingBlockSpeciesLimit
        fields = "__all__"
