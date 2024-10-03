from rest_framework import serializers
from bm_hunting_settings.models import  Species

class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = '__all__'  
