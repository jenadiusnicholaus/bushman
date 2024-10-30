from rest_framework import serializers
from bm_hunting_settings.models import (
    HuntingPackageCustomization,
    HuntingPackageCustomizedSpecies,
)


class GetCustomzedPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuntingPackageCustomization
        fields = "__all__"


class CreateCustomizedPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuntingPackageCustomization
        fields = "__all__"


class UpdateCustomizedPackageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = HuntingPackageCustomization


# -----------------hunting package customized species serializer -----------------
class GetCustomizedSpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuntingPackageCustomizedSpecies
        fields = "__all__"


class CreateCustomizedSpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuntingPackageCustomizedSpecies
        fields = "__all__"


class UpdateCustomizedSpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuntingPackageCustomizedSpecies
        fields = "__all__"
