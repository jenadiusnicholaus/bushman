from bm_hunting_settings.models import (
    HuntingArea,
    HuntingQuatasArea,
    Quota,
    QuotaHutingAreaSpecies,
)
from rest_framework import serializers


class GetQuotaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quota
        fields = "__all__"


class CreateQuotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quota
        fields = "__all__"


class UpdateQuotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quota
        fields = "__all__"


# -----------hunting area quota serializers-


class GetHuntingQuatasAreaSerializers(serializers.ModelSerializer):
    class Meta:
        model = HuntingQuatasArea
        fields = "__all__"


class CreateHuntingQuatasAreaSerializers(serializers.ModelSerializer):
    class Meta:
        model = HuntingQuatasArea
        fields = "__all__"


class UpdateHuntingQuatasAreaSerializers(serializers.ModelSerializer):
    class Meta:
        model = HuntingQuatasArea
        fields = "__all__"


# -----------species quota serializers-
class QuotaHutingAreaSpeciesSerializers(serializers.ModelSerializer):
    class Meta:
        model = QuotaHutingAreaSpecies
        fields = "__all__"
        depth = 2


class CreateQuotaHutingAreaSpeciesSerializers(serializers.ModelSerializer):
    class Meta:
        model = QuotaHutingAreaSpecies
        fields = "__all__"


class UpdateQuotaHutingAreaSpeciesSerializers(serializers.ModelSerializer):
    class Meta:
        model = QuotaHutingAreaSpecies
        fields = "__all__"
