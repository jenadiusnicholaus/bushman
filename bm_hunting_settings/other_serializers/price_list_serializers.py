from rest_framework import serializers

from bm_hunting_settings.models import (
    HuntingPackageCompanionsHunter,
    HuntingPackageOberverHunter,
    HuntingPackageUpgradeFees,
    HuntingPriceList,
    HuntingPriceListType,
    HuntingPriceTypePackage,
    HuntingType,
    SalesPackages,
    SalesPackageSpecies,
)
from bm_hunting_settings.serializers import HutingAreaSerializers, SpeciesSerializer


# ----------------HuntingType Serializer----------------
class GetHuntingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuntingType
        fields = "__all__"


class CreateHuntingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuntingType
        fields = "__all__"


class UpdateHuntingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuntingType
        fields = "__all__"


# ---------------SalesPackage Serializer----------------
class GetSalesPackageSerializer(serializers.ModelSerializer):
    species = serializers.SerializerMethodField()

    class Meta:
        model = SalesPackages
        # fields = "__all__"
        depth = 1
        exclude = ["user"]

    def get_species(self, obj):
        species = obj.sales_package_species.all()
        if len(species) == 0:
            return []
        serializer = GetSalesPackageSpeciesSerializer(species, many=True)
        return serializer.data


class CreateSalesPackageSerializer(serializers.ModelSerializer):

    class Meta:
        model = SalesPackages
        fields = "__all__"


class UpdateSalesPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesPackages
        fields = "__all__"


# ------------------HuntingPriceList-------------------


class GetHuntingPriceListSerializer(serializers.ModelSerializer):
    area = HutingAreaSerializers()

    class Meta:
        model = HuntingPriceList
        fields = ["area"]


class CreateHuntingPriceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuntingPriceList
        fields = "__all__"


class UpdateHuntingPriceListSerializer(serializers.ModelSerializer):

    class Meta:
        model = HuntingPriceList
        fields = "__all__"


# ------------------HuntingPriceListType-------------------


class GetHuntingPriceListTypeSerializer(serializers.ModelSerializer):
    price_list = GetHuntingPriceListSerializer()
    hunting_type = GetHuntingTypeSerializer()
    currency = serializers.CharField(source="currency.symbol")

    class Meta:

        model = HuntingPriceListType
        fields = "__all__"
        # depth = 2
        # exclude = ["user"]


class CreateHuntingPriceListTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuntingPriceListType
        fields = "__all__"
        # depth = 2


class UpdateHuntingPriceListTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = HuntingPriceListType
        fields = "__all__"


# ------------------HƒuntingPriceTypePackage-=------------------------


class GetHuntingPriceTypePackageSerializer(serializers.ModelSerializer):
    sales_package = GetSalesPackageSerializer()
    price_list_type = GetHuntingPriceListTypeSerializer()
    componions_hunter = serializers.SerializerMethodField()
    oberver = serializers.SerializerMethodField()

    def get_componions_hunter(self, obj):
        componions_hunter = obj.hunting_package_companions_hunter.all()
        if len(componions_hunter) == 0:
            return []
        serializer = GetHuntingPackageCompanionsHunterSerializer(
            componions_hunter, many=True
        )
        return serializer.data

    def get_oberver(self, obj):
        oberver = obj.hunting_package_oberver_hunter.all()
        if len(oberver) == 0:
            return []
        serializer = GetHuntingPackageOberverHunterSerializer(oberver, many=True)
        return serializer.data

    class Meta:
        model = HuntingPriceTypePackage
        fields = "__all__"
        # depth = 2


class CreateHuntingPriceTypePackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuntingPriceTypePackage
        fields = "__all__"


class UpdateHuntingPriceTypePackageSerializer(serializers.ModelSerializer):

    class Meta:
        model = HuntingPriceTypePackage
        fields = "__all__"


# ------------------salesPackageSpecies-=------------------


class GetSalesPackageSpeciesSerializer(serializers.ModelSerializer):
    species = SpeciesSerializer()

    class Meta:
        model = SalesPackageSpecies
        fields = "__all__"


class CreateSalesPackageSpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesPackageSpecies
        fields = "__all__"


class UpdateSalesPackageSpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesPackageSpecies
        fields = "__all__"


# ------------------HuntingPackageUpgradeFeesSerializer------------------


class GetHuntingPackageUpgradeFeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuntingPackageUpgradeFees
        fields = "__all__"


class CreateHuntingPackageUpgradeFeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuntingPackageUpgradeFees
        fields = "__all__"


class UpdateHuntingPackageUpgradeFeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuntingPackageUpgradeFees
        fields = "__all__"


# ------------------HuntingPackageCompanionsHunter----------------


class GetHuntingPackageCompanionsHunterSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuntingPackageCompanionsHunter
        fields = "__all__"


class CreateHuntingPackageCompanionsHunterSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuntingPackageCompanionsHunter
        fields = "__all__"


class UpdateHuntingPackageCompanionsHunterSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuntingPackageCompanionsHunter
        fields = "__all__"


# ---------------------- Hunting package Oberver Cost--------------
class GetHuntingPackageOberverHunterSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuntingPackageOberverHunter
        fields = "__all__"


class CreateHuntingPackageOberverHunterSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuntingPackageOberverHunter
        fields = "__all__"


class UpdateHuntingPackageOberverHunterSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuntingPackageOberverHunter
        fields = "__all__"


# ====== additional cost serializers ======#

# class GetAdditionalServices
