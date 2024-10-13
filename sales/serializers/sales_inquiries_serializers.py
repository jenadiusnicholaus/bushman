from rest_framework import serializers
from django_countries.serializer_fields import CountryField


from bm_hunting_settings.serializers import (
    CountrySerializeers,
    NationalitiesSerializeers,
)
from sales.models import (
    Contacts,
    Entity,
    EntityCategory,
    SalesInquiry,
    SalesIquiryPreference,
)

# from sales.views.sales_inquiries_views import SalesInquiriesViewSet


class GetEntitySerializers(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    country = CountrySerializeers()
    sales_inquiry = serializers.SerializerMethodField()
    nationality = NationalitiesSerializeers()

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

    def get_sales_inquiry(self, obj):
        try:
            sales_inquiry = obj.sales_inquiry_entity_set.get()
            if sales_inquiry:
                sez = GetSalesInquirySerializers(sales_inquiry)
                return sez.data
            else:
                return None
        except:
            return None

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


# -------------------------- Sales Inquiry Serializers ---------- #
class GetSalesInquirySerializers(serializers.ModelSerializer):
    class Meta:
        model = SalesInquiry
        fields = "__all__"


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





