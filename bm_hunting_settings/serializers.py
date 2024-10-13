from rest_framework import serializers
from bm_hunting_settings.models import (
    AccommodationType,
    Country,
    HuntingArea,
    Nationalities,
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
