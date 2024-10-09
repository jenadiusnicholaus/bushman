from rest_framework import serializers
from bm_hunting_settings.models import HuntingBlock, Species
from sales.models import EntityCategories, EntityCategory


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


# =============enting EntityCategorySerializer========
class GetHuntingBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuntingBlock
        fields = "__all__"


class CreateHuntingBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuntingBlock
        fields = "__all__"


class UpdateHuntingBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuntingBlock
        fields = "__all__"


class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = "__all__"
