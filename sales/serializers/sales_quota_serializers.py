from bm_hunting_settings.models import Quota
from rest_framework import serializers


class GetQuotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quota        
        fields = '__all__'

class CreateQuotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quota
        fields = '__all__'

class UpdateQuotaSerializer(serializers.ModelSerializer):
   class Meta:
       model = Quota
       fields = '__all__'