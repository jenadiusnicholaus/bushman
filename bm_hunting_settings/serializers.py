from rest_framework import serializers
from bm_hunting_settings.models import (
    AccommodationType,
    Country,
    Currency,
    GeoLocationCoordinates,
    HuntingArea,
    Locations,
    Nationalities,
    RegulatoryHuntingPackageSpecies,
    RegulatoryHuntingpackage,
    Seasons,
    Species,
)
from sales.models import (
    ContactType,
    Doctype,
    EntityCategories,
    EntityCategory,
    PaymentMethod,
)


class GetCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"


class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = "__all__"


class EntityCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityCategories
        fields = "__all__"


class CreateEntityCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityCategory
        fields = "__all__"


class CountrySerializeers(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class NationalitiesSerializeers(serializers.ModelSerializer):
    class Meta:
        model = Nationalities
        fields = "__all__"


# --- contact types ---
class GetContactTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactType
        fields = "__all__"


# --- accommodation  types---


class GetAccommodationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccommodationType
        fields = "__all__"


class GetPaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = "__all__"


# -----------hunting area serializers-
class HutingAreaSerializers(serializers.ModelSerializer):
    class Meta:
        model = HuntingArea
        fields = "__all__"
        depth = 3


class CreateHutingAreaSerializers(serializers.ModelSerializer):
    class Meta:
        model = HuntingArea
        fields = "__all__"


class UpdateHutingAreaSerializers(serializers.ModelSerializer):
    class Meta:
        model = HuntingArea
        fields = "__all__"


# -----------geo location -------


class GetGeoLocationsSerializers(serializers.ModelSerializer):
    class Meta:
        model = GeoLocationCoordinates

        fields = "__all__"


class CreateGeoLocationsSerializers(serializers.ModelSerializer):
    class Meta:
        model = GeoLocationCoordinates
        fields = "__all__"


class UpdateGeoLocationsSerializers(serializers.ModelSerializer):
    class Meta:
        model = GeoLocationCoordinates
        fields = "__all__"


# -----------location serializers-------


class GetLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = "__all__"


class CreateLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = "__all__"


class UpdateLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = "__all__"


# ----------- regulatory hunting packag serializers-
class GetRegulatoryHuntingPackageSerializers(serializers.ModelSerializer):
    class Meta:
        model = RegulatoryHuntingpackage
        fields = "__all__"
        # depth = 1


class CreateRegulatoryHuntingPackageSerializers(serializers.ModelSerializer):
    class Meta:
        model = RegulatoryHuntingpackage
        fields = "__all__"


class UpdateRegulatoryHuntingPackageSerializers(serializers.ModelSerializer):
    class Meta:
        model = RegulatoryHuntingpackage
        fields = "__all__"


# ----------- regulatory hunting packag Species serializers-------


class GetRegulatoryHuntingPackageSpeciesSerializers(serializers.ModelSerializer):
    species = SpeciesSerializer()

    class Meta:
        model = RegulatoryHuntingPackageSpecies

        fields = "__all__"


class CreateRegulatoryHuntingPackageSpeciesSerializers(serializers.ModelSerializer):
    class Meta:
        model = RegulatoryHuntingPackageSpecies
        fields = "__all__"


class UpdateRegulatoryHuntingPackageSpeciesSerializers(serializers.ModelSerializer):
    class Meta:
        model = RegulatoryHuntingPackageSpecies
        fields = "__all__"


# ---------------------- seasons--------------
class GetSeasonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seasons
        fields = "__all__"


class CreateSeasonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seasons
        fields = "__all__"


class UpdateSeasonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seasons
        fields = "__all__"


# ---------- Doctype--------------


class GetDoctypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctype
        fields = "__all__"
