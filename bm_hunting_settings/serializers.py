from rest_framework import serializers
from bm_hunting_settings.models import (
    AccommodationType,
    Country,
    GeoLocationCoordinates,
    HuntingArea,
    Locations,
    Nationalities,
    RegulatoryHuntingPackageSpecies,
    RegulatoryHuntingpackage,
    Species,
)
from sales.models import ContactType, EntityCategories, EntityCategory, PaymentMethod


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
        fields = [
            "id",
            "name",
            "quota",
        ]
        depth = 1


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
