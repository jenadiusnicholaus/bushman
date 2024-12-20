from rest_framework import serializers
from django_countries.serializer_fields import CountryField


from bm_hunting_settings.serializers import (
    CountrySerializeers,
    HutingAreaSerializers,
    NationalitiesSerializeers,
)
from sales.models import (
    Contacts,
    Entity,
    EntityCategory,
    EntityIdentity,
    SalesInquiry,
    SalesInquiryArea,
    SalesInquiryPriceList,
    SalesInquirySpecies,
    SalesIquiryPreference,
)

# from sales.views.sales_inquiries_views import SalesInquiriesViewSet


class GetEntitySerializers(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    country = CountrySerializeers()
    # sales_inquiry = serializers.SerializerMethodField()
    nationality = NationalitiesSerializeers()
    contacts = serializers.SerializerMethodField()

    def get_category(self, obj):
        try:
            category = obj.entity_category.get()
            if category:
                sez = EntityCategorySerializers(category)
                return sez.data
            else:
                return None
        except:
            return None

    def get_contacts(self, obj):
        contants = obj.entity_contacts_set.all()
        if contants:
            sez = GetContactsSerializers(contants, many=True)
            return sez.data

    class Meta:
        model = Entity
        fields = "__all__"


class CreateEntitySerializers(serializers.ModelSerializer):

    class Meta:
        model = Entity
        fields = "__all__"


class UpdateEntitySerializers(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = "__all__"


# ---------- Entity Category Serializers ---------- #
class EntityCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = EntityCategory
        fields = "__all__"
        depth = 0


# ----------- Entity Category Serializers ---------- #
class CreateEntityCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = EntityCategory
        fields = "__all__"


class GetEntityIdentitySerializers(serializers.ModelSerializer):
    class Meta:
        model = EntityIdentity
        fields = "__all__"
        depth = 1


class CreateEntityIdentitySerializers(serializers.ModelSerializer):
    class Meta:
        model = EntityIdentity
        fields = "__all__"


class UpdateEntityIdentitySerializers(serializers.ModelSerializer):
    class Meta:
        model = EntityIdentity
        fields = "__all__"


# -------------------------- Sales Inquiry Serializers ---------- #
class GetSalesInquirySerializers(serializers.ModelSerializer):
    entity = GetEntitySerializers()
    preference = serializers.SerializerMethodField()
    preferred_species = serializers.SerializerMethodField()
    area = serializers.SerializerMethodField()
    entity_identity = serializers.SerializerMethodField()
    price_list = serializers.SerializerMethodField()

    def get_area(self, obj):
        try:
            area = obj.hunting_inquiry_area_set.all()
            if len(area) > 0:
                sez = GetSalesInquiryAreaSerializer(area, many=True)
                return sez.data
            else:
                return []
        except:
            return []

    class Meta:
        model = SalesInquiry
        fields = "__all__"

    def get_preferred_species(self, obj):
        try:
            species = obj.sales_inquiry_species_set.all()
            if len(species) > 0:
                sez = GetSalesInquirySpeciesSerializer(species, many=True)
                return sez.data
            else:
                return []
        except:
            return []

    def get_preference(self, obj):

        preferences = (
            obj.sales_inquiry_preference_set.all()
        )  # Get all related preferences
        if preferences.exists():  # Check if any preferences exist
            preference = preferences.latest("create_date")
            sez = SalesIquiryPreferenceSerializers(preference)
            return sez.data
        else:
            return None

    def get_entity_identity(self, obj):
        try:
            identity = EntityIdentity.objects.get(entity=obj.entity)
            if identity:
                sez = GetEntityIdentitySerializers(identity)
                return sez.data
            else:
                return None
        except:
            return None

    def get_price_list(self, obj):
        try:
            price_list = SalesInquiryPriceList.objects.get(sales_inquiry=obj)
            if price_list:
                sez = GetSalesInquiryPriceListSerializer(price_list)
                return sez.data
            else:
                return None
        except:
            return None


class CreateSalesInquirySerializers(serializers.ModelSerializer):
    class Meta:
        model = SalesInquiry
        fields = "__all__"


class UpdateSalesInquirySerializers(serializers.ModelSerializer):
    class Meta:
        model = SalesInquiry
        fields = "__all__"


# # ----------- Sales Inquiry preference Serializers ---------- #
class SalesIquiryPreferenceSerializers(serializers.ModelSerializer):
    class Meta:
        model = SalesIquiryPreference
        fields = "__all__"


class CreateSalesIquiryPreferenceSerializers(serializers.ModelSerializer):
    class Meta:
        model = SalesIquiryPreference
        fields = "__all__"


class UpdateSalesIquiryPreferenceSerializers(serializers.ModelSerializer):
    class Meta:
        model = SalesIquiryPreference
        fields = "__all__"


# --------------- Contacts Serializers ---------- #
class GetContactsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = "__all__"


class CreateContactsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = "__all__"


class UpdateContactsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = "__all__"


class GetSalesInquirySpeciesSerializer(serializers.ModelSerializer):

    class Meta:
        model = SalesInquirySpecies
        fields = "__all__"
        depth = 1


class CreateSalesInquirySpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesInquirySpecies
        fields = "__all__"


class UpdateSalesInquirySpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesInquirySpecies
        fields = "__all__"


# ---------- Sales Inquiry Area Serializers ---------- #
class GetSalesInquiryAreaSerializer(serializers.ModelSerializer):
    area = HutingAreaSerializers()

    class Meta:
        model = SalesInquiryArea
        fields = "__all__"


class CreateSalesInquiryAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesInquiryArea
        fields = "__all__"


class UpdateSalesInquiryAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesInquiryArea
        fields = "__all__"


# sales inquiry price list serializer


class GetSalesInquiryPriceListSerializer(serializers.ModelSerializer):

    class Meta:
        model = SalesInquiryPriceList
        fields = "__all__"


class createSalesInquiryPriceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesInquiryPriceList
        fields = "__all__"


class UpdateSalesInquiryPriceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesInquiryPriceList
        fields = "__all__"
