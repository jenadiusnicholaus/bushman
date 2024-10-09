from rest_framework import serializers
from django_countries.serializer_fields import CountryField


from sales.models import Entity, EntityCategory


class GetEntitySerializers(serializers.ModelSerializer):
    country = CountryField(country_dict=True)
    category = serializers.SerializerMethodField()

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


class EntityCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = EntityCategory
        fields = "__all__"
        depth = 1


class CreateEntityCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = EntityCategory
        fields = "__all__"
