from rest_framework import serializers

from bm_hunting_settings.models import (
    HuntingPackageCompanionsHunter,
    HuntingPackageUpgradeFees,
    HuntingPriceList,
    HuntingPriceListType,
    HuntingPriceTypePackage,
    HuntingType,
    SalesPackage,
    SalesPackageSpecies,
)


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

    class Meta:
        model = SalesPackage
        fields = "__all__"


class CreateSalesPackageSerializer(serializers.ModelSerializer):

    class Meta:
        model = SalesPackage
        fields = "__all__"


class UpdateSalesPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesPackage
        fields = "__all__"


# ------------------HuntingPriceList-------------------


class GetHuntingPriceListSerializer(serializers.ModelSerializer):
    hunting_price_list_type = serializers.SerializerMethodField()

    def get_hunting_price_list_type(self, obj):
        try:
            price_list_type = obj.hunting_price_list_type.all()
            serializer = GetHuntingPriceListTypeSerializer(price_list_type, many=True)
            return serializer.data
        except:

            return None

    class Meta:
        model = HuntingPriceList
        # fields = "__all__"
        depth = 2
        exclude = ["user"]


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
    hunting_type = GetHuntingTypeSerializer()
    packages = serializers.SerializerMethodField()

    def get_packages(self, obj):
        try:
            price_list_type = obj.hunting_price_type_package.all()
            serializer = GetHuntingPriceTypePackageSerializer(
                price_list_type, many=True
            )
            return serializer.data
        except:
            return None

    class Meta:

        model = HuntingPriceListType
        fields = "__all__"
        # depth = 2
        # exclude = ["user"]


class CreateHuntingPriceListTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuntingPriceListType
        fields = "__all__"


class UpdateHuntingPriceListTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuntingPriceListType
        fields = "__all__"


# ------------------HuntingPriceTypePackage-=------------------------


class GetHuntingPriceTypePackageSerializer(serializers.ModelSerializer):
    sales_package = GetSalesPackageSerializer()

    class Meta:
        model = HuntingPriceTypePackage
        fields = "__all__"


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
    class Mata:
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
        field = "__all__"


class CreateHuntingPackageCompanionsHunterSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuntingPackageCompanionsHunter
        fields = "__all__"


# ====== additional cost serializers ======#

# class GetAdditionalServices
