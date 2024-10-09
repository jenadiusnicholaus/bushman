from rest_framework import serializers

from sales.models import Document


class GetClientsDocsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = "__all__"


class CreateClientsDocsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"
