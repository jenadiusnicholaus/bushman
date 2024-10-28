from authentication import models
from bm_hunting_settings.models import (
    HuntingArea,
    HuntingQuatasArea,
    Quota,
    QuotaHutingAreaSpecies,
)
from rest_framework import serializers

from sales.models import SalesInquirySpecies
from sales_confirmation.models import (
    SalesConfirmationProposal,
    SalesConfirmationProposalStatus,
)


class GetQuotaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quota
        fields = "__all__"


class CreateQuotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quota
        fields = "__all__"


class UpdateQuotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quota
        fields = "__all__"


# -----------hunting area quota serializers-


class GetHuntingQuatasAreaSerializers(serializers.ModelSerializer):
    class Meta:
        model = HuntingQuatasArea
        fields = "__all__"


class CreateHuntingQuatasAreaSerializers(serializers.ModelSerializer):
    class Meta:
        model = HuntingQuatasArea
        fields = "__all__"


class UpdateHuntingQuatasAreaSerializers(serializers.ModelSerializer):
    class Meta:
        model = HuntingQuatasArea
        fields = "__all__"


# -----------species quota serializers-
class QuotaHutingAreaSpeciesSerializers(serializers.ModelSerializer):
    # STATUS = (
    #     ("pending", "Pending"),
    #     ("provision_sales", "Provision Sales"),
    #     ("confirmed", "Confirmed"),
    #     ("declined", "Declined"),
    #     ("cancelled", "Cancelled"),
    #     ("completed", "Completed"),
    # )
    provision_quantity = serializers.SerializerMethodField()
    confirmed_quantity = serializers.SerializerMethodField()
    declined_quantity = serializers.SerializerMethodField()
    cancelled_quantity = serializers.SerializerMethodField()
    completed_quantity = serializers.SerializerMethodField()

    class Meta:
        model = QuotaHutingAreaSpecies
        fields = "__all__"
        depth = 1

    def get_provision_quantity(self, obj):
        quantity = 0
        status = obj.species.species_sales_species_status_set.filter(
            status="provision_sales"
        )

        if status.exists():
            for i in status:

                quantity += i.quantity

        return quantity

    def get_confirmed_quantity(self, obj):
        quantity = 0
        status = obj.species.species_sales_species_status_set.filter(status="confirmed")
        if status.exists():
            for i in status:

                quantity += i.quantity

        return quantity

    def get_declined_quantity(self, obj):
        quantity = 0
        status = obj.species.species_sales_species_status_set.filter(status="declined")
        if status.exists():
            for i in status:

                quantity += i.quantity

        return quantity

    def get_cancelled_quantity(self, obj):
        quantity = 0
        status = obj.species.species_sales_species_status_set.filter(status="cancelled")
        if status.exists():
            for i in status:

                quantity += i.quantity

        return quantity

    def get_completed_quantity(self, obj):
        quantity = 0
        status = obj.species.species_sales_species_status_set.filter(status="completed")
        if status.exists():
            for i in status:

                quantity += i.quantity
        return quantity


class CreateQuotaHutingAreaSpeciesSerializers(serializers.ModelSerializer):
    class Meta:
        model = QuotaHutingAreaSpecies
        fields = "__all__"


class UpdateQuotaHutingAreaSpeciesSerializers(serializers.ModelSerializer):
    class Meta:
        model = QuotaHutingAreaSpecies
        fields = "__all__"
