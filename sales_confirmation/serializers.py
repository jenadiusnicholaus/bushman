from rest_framework import serializers

from sales.serializers.sales_inquiries_serializers import GetSalesInquirySerializers
from sales_confirmation.models import (
    SalesConfirmationProposal,
    SalesConfirmationProposalAdditionalService,
    SalesConfirmationProposalItinerary,
    SalesConfirmationProposalPackage,
)


# ------------------ SalesConfirmationProposal Serializer ------------------ #
class GetSalesConfirmationProposalSerializer(serializers.ModelSerializer):
    sales_inquiry = GetSalesInquirySerializers()
    proposed_package = serializers.SerializerMethodField()
    itinerary = serializers.SerializerMethodField()
    additional_services = serializers.SerializerMethodField()

    class Meta:
        model = SalesConfirmationProposal
        fields = "__all__"

    def get_proposed_package(self, obj):
        # Assuming sales_confirmation_package is a one-to-one field
        try:
            package = obj.sales_confirmation_package
            if package:  # if package exists
                return GetSalesConfirmationProposalPackageSerializer(package).data
            return None
        except:
            return None

    def get_itinerary(self, obj):
        # Assuming itineraries is a one-to-one field
        try:
            itinerary = obj.itineraries  # Change this to 'itinerary' if it's one-to-one
            if itinerary:  # if itinerary exists
                return SalesConfirmationProposalItinerarySerializer(itinerary).data
            return None
        except:
            return None

    def get_additional_services(self, obj):

        additional_services = obj.additional_services.all()
        if len(additional_services) > 0:  # check if additional services exist
            return GetSalesConfirmationProposalAdditionalServiceSerializer(
                additional_services,
                many=True,  # Use many=True if this is a queryset/list
            ).data
        return None


class CreateSalesConfirmationProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesConfirmationProposal
        fields = "__all__"


class UpdateSalesConfirmationProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesConfirmationProposal
        fields = "__all__"


# -------------------- SalesConfirmationProposal Serializer ------------------ #


class GetSalesConfirmationProposalPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesConfirmationProposalPackage
        fields = "__all__"


class CreateSalesConfirmationProposalPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesConfirmationProposalPackage
        fields = "__all__"


class UpdateSalesConfirmationProposalPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesConfirmationProposalPackage
        fields = "__all__"


# ------------------ SalesConfirmationProposalItinerary Serializer ------------------ #


class SalesConfirmationProposalItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesConfirmationProposalItinerary
        fields = "__all__"


class CreateSalesConfirmationProposalItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesConfirmationProposalItinerary
        fields = "__all__"


class UpdateSalesConfirmationProposalItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesConfirmationProposalItinerary
        fields = "__all__"


# ---------- SalesConfirmationProposalItinerary Serializer ------------------ #


class GetSalesConfirmationProposalAdditionalServiceSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = SalesConfirmationProposalAdditionalService
        fields = "__all__"


class CreateSalesConfirmationProposalAdditionalServiceSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = SalesConfirmationProposalAdditionalService
        fields = "__all__"


class UpdateSalesConfirmationProposalAdditionalServiceSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = SalesConfirmationProposalAdditionalService
        fields = "__all__"
