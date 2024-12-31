from rest_framework import serializers

from bm_hunting_settings.models import HuntingPriceTypePackage
from bm_hunting_settings.other_serializers.price_list_serializers import (
    GetHuntingPriceTypePackageSerializer,
    GetSalesPackageSerializer,
)
from bm_hunting_settings.serializers import (
    GetLocationSerializer,
    GetRegulatoryHuntingPackageSerializers,
    GetSafaryExtrasSerializer,
    GetSalesChartersPriceListSerializer,
    HutingAreaSerializers,
    SpeciesSerializer,
)
from sales.models import Document
from sales.serializers.sales_inquiries_serializers import (
    GetEntitySerializers,
    GetSalesInquirySerializers,
)
from sales_confirmation.models import (
    AccommodationAddress,
    AccommodationCost,
    AccommodationType,
    EntityContractPermitDates,
    EntityContractPermit,
    GameActivity,
    GameActivityProfessionalHunter,
    GameKilledActivity,
    Installment,
    SalesConfirmationAccommodation,
    SalesConfirmationChartersPriceList,
    SalesConfirmationCompanions,
    SalesConfirmationContract,
    SalesConfirmationProposal,
    SalesConfirmationProposalAdditionalService,
    SalesConfirmationProposalCompanionItinerary,
    SalesConfirmationProposalItinerary,
    SalesConfirmationProposalObserver,
    SalesConfirmationProposalPackage,
    SalesConfirmationProposalSafaryExtras,
    SalesConfirmationProposalStatus,
    SalesQuotaSpeciesStatus,
)
from utils.pdf import SalesConfirmationPDF
from utils.sales_price_breakdown import calculate_total_cost
from django.urls import reverse


# ------------------ SalesConfirmationProposal Serializer ------------------ #
class GetSalesConfirmationProposalSerializer(serializers.ModelSerializer):
    sales_inquiry = GetSalesInquirySerializers()
    proposed_package = serializers.SerializerMethodField()
    itinerary = serializers.SerializerMethodField()
    additional_services = serializers.SerializerMethodField()
    installments = serializers.SerializerMethodField()
    price_break_down = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    # pdf = serializers.SerializerMethodField()
    regulatory_package = GetRegulatoryHuntingPackageSerializers()

    class Meta:
        model = SalesConfirmationProposal
        fields = "__all__"

    def get_proposed_package(self, obj):
        # Assuming sales_confirmation_package is a one-to-one field
        try:
            package = obj.sales_confirmation_package
            package_type = HuntingPriceTypePackage.objects.filter(
                sales_package__id=package.package.id
            ).first()
            if package_type is None:
                return None

            # Serialize both package type and sales confirmation package
            sz1 = GetHuntingPriceTypePackageSerializer(package_type).data
            sz2 = GetSalesConfirmationProposalPackageSerializer(package).data

            if sz1 and sz2:
                # Combine the serialized data
                return {**sz1, **sz2}
            return None
        except Exception as e:
            # Log the error if necessary
            print(f"Error in get_proposed_package: {e}")
            return None

    def get_all_proposed_packages(self, objects):
        proposed_packages = []
        for obj in objects:
            proposed_package = self.get_proposed_package(obj)
            if proposed_package is not None:
                proposed_packages.append(
                    proposed_package
                )  # Ensure this is a serializable structure
        return proposed_packages

    # Usage
    # proposed_packages = get_all_proposed_packages(your_objects_list)

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

    def get_installments(self, obj):
        installments = obj.installments.all()
        if len(installments) > 0:
            return GetInstallmentSerializer(installments, many=True).data
        else:
            return []

    def get_price_break_down(self, obj):
        try:
            sales_inquiry_id = obj.sales_inquiry.id
            package_id = obj.sales_confirmation_package.package.id
            response_data = calculate_total_cost(
                sales_inquiry_id=sales_inquiry_id, package_id=package_id
            )
            return response_data
        except:
            return None

    def get_status(self, obj):
        try:
            status = obj.status
            return GetSalesConfirmationProposalStatusSerializer(status).data
        except:
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
    package = GetSalesPackageSerializer()

    class Meta:
        model = SalesConfirmationProposalPackage
        fields = "__all__"
        # depth = 6


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


# -------------------- Installment Serializer ------------------ #
class GetInstallmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Installment
        fields = "__all__"


class CreateInstallmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Installment
        fields = "__all__"


class UpdateInstallmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Installment
        fields = "__all__"


# ------------------- upload doc serializer - #


class GetDocSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"


class UploadDocSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"


class UpdateDocSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document


# --------------status serializer- #
class GetSalesConfirmationProposalStatusSerializer(serializers.ModelSerializer):
    document = GetDocSerializer()
    # sales_confirmation_proposal = GetSalesConfirmationProposalSerializer()

    class Meta:
        model = SalesConfirmationProposalStatus
        fields = "__all__"


class CreateSalesConfirmationProposalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesConfirmationProposalStatus
        fields = "__all__"


class UpdateSalesConfirmationProposalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesConfirmationProposalStatus
        fields = "__all__"


# --------------status serializer- #
class GetSalesQuotaSpeciesStatusSerializer(serializers.ModelSerializer):
    sales_proposal = GetSalesConfirmationProposalSerializer()

    class Meta:
        model = SalesQuotaSpeciesStatus
        fields = "__all__"


class CreateSalesQuotaSpeciesStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesQuotaSpeciesStatus
        fields = "__all__"


class UpdateSalesQuotaSpeciesStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesQuotaSpeciesStatus
        fields = "__all__"


# ------------------Sales Confirmation contract ------------------ #


class GetSalesConfirmationContractSerializer(serializers.ModelSerializer):
    sales_confirmation_proposal = GetSalesConfirmationProposalSerializer()
    entity = GetEntitySerializers()

    class Meta:
        model = SalesConfirmationContract
        fields = "__all__"


class CreateSalesConfirmationContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesConfirmationContract
        fields = "__all__"


class UpdateSalesConfirmationContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesConfirmationContract
        fields = "__all__"


# -------------------- EnityContractPermit -------------------


class GetEntityContractPermitSerializer(serializers.ModelSerializer):
    dates = serializers.SerializerMethodField()
    entity_contract = GetSalesConfirmationContractSerializer()
    package_type = GetRegulatoryHuntingPackageSerializers()

    class Meta:
        model = EntityContractPermit
        fields = "__all__"

    def get_dates(self, obj):
        dates_obj = obj.contract_dates_set.all()
        if len(dates_obj) > 0:
            return GetEntityContractPermitDatesSerializer(dates_obj, many=True).data
        else:
            return []


class CreateEntityContractPermitSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityContractPermit
        fields = "__all__"


class UpdateEntityContractPermitSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityContractPermit
        fields = "__all__"


# ======================== EntityContactDates ===============


class GetEntityContractPermitDatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityContractPermitDates
        fields = "__all__"


class CreateEntityContractPermitDatesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityContractPermitDates
        fields = "__all__"


class UpdateEntityContractPermitDatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityContractPermitDates
        fields = "__all__"


# ------------------ GameActivity serializer - #
class GetGameActivitySerializer(serializers.ModelSerializer):
    entity_contract_permit = GetEntityContractPermitSerializer()
    client = GetEntitySerializers()
    ph = serializers.SerializerMethodField()
    game_killed_activity = serializers.SerializerMethodField()

    class Meta:
        model = GameActivity
        fields = "__all__"

    def get_ph(self, obj):
        ph_obj = obj.professional_hunter_set.all()
        if len(ph_obj) > 0:
            return GetGameActivityProfessionalHunterSerializer(ph_obj, many=True).data
        else:
            return []

    def get_game_killed_activity(self, obj):
        game_killed_activity_obj = obj.game_killed_activity_set.all()
        if len(game_killed_activity_obj) > 0:
            return GetGameKilledActivitySerializer(
                game_killed_activity_obj, many=True
            ).data
        else:
            return []


class CreateGameActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = GameActivity
        fields = "__all__"


class UpdateGameActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = GameActivity
        fields = "__all__"


# ----------------- GameKilledActivity serializer ----------------- #
class GetGameKilledActivitySerializer(serializers.ModelSerializer):
    species = SpeciesSerializer()
    location = GetLocationSerializer()
    area = HutingAreaSerializers()

    class Meta:
        model = GameKilledActivity
        fields = "__all__"


class CreateGameKilledActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = GameKilledActivity
        fields = "__all__"


class UpdateGameKilledActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = GameKilledActivity
        fields = "__all__"


class GetGameActivityProfessionalHunterSerializer(serializers.ModelSerializer):
    ph = GetEntitySerializers()

    class Meta:
        model = GameActivityProfessionalHunter
        fields = "__all__"


class CreateGameActivityProfessionalHunterSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameActivityProfessionalHunter
        fields = "__all__"


class UpdateGameActivityProfessionalHunterSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameActivityProfessionalHunter
        fields = "__all__"


# ------------------- SalesConfirmationPDF serializer - #
class GetSalesConfirmationCompanionsSerializer(serializers.ModelSerializer):
    companion = GetEntitySerializers()
    regulatory_package = GetRegulatoryHuntingPackageSerializers()

    class Meta:
        model = SalesConfirmationCompanions
        fields = "__all__"


class CreateSalesConfirmationCompanionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesConfirmationCompanions
        fields = "__all__"


class UpdateSalesConfirmationCompanionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesConfirmationCompanions
        fields = "__all__"


#  ------------------- observer serializer ----------------------
class GetSalesConfirmationProposalObserverSerializer(serializers.ModelSerializer):
    observer = GetEntitySerializers()

    class Meta:
        model = SalesConfirmationProposalObserver
        fields = "__all__"


class CreateSalesConfirmationProposalObserverSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesConfirmationProposalObserver
        fields = "__all__"


class UpdateSalesConfirmationProposalObserverSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesConfirmationProposalObserver
        fields = "__all__"


# --------------------- companion itinerary serializer - #
class GetSalesConfirmationProposalCompanionItinerarySerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = SalesConfirmationProposalCompanionItinerary
        fields = "__all__"


class CreateSalesConfirmationProposalCompanionItinerarySerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = SalesConfirmationProposalCompanionItinerary
        fields = "__all__"


class UpdateSalesConfirmationProposalCompanionItinerarySerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = SalesConfirmationProposalCompanionItinerary
        fields = "__all__"


class GetSalesConfirmationProposalSafaryExtrasSerializer(serializers.ModelSerializer):
    safari_extras = GetSafaryExtrasSerializer()

    class Meta:
        model = SalesConfirmationProposalSafaryExtras
        fields = "__all__"


class CreateSalesConfirmationProposalSafaryExtrasSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = SalesConfirmationProposalSafaryExtras
        fields = "__all__"


class UpdateSalesConfirmationProposalSafaryExtrasSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = SalesConfirmationProposalSafaryExtras
        fields = "__all__"


# - AccommodationType- #
class GetAccommodationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccommodationType
        fields = "__all__"


class CreateAccommodationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccommodationType
        fields = "__all__"


class UpdateAccommodationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccommodationType
        fields = "__all__"


class GetAccommodationAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccommodationAddress
        fields = "__all__"


class CreateAccommodationAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccommodationAddress
        fields = "__all__"


class UpdateAccommodationAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccommodationAddress
        fields = "__all__"


class GetSalesConfirmationAccommodationSerializer(serializers.ModelSerializer):
    entity = GetEntitySerializers()
    type = GetAccommodationTypeSerializer()
    address = GetAccommodationAddressSerializer()
    cost = serializers.SerializerMethodField()

    def get_cost(self, obj):
        cost_obj = obj.accommodation_cost_set.all()
        if len(cost_obj) > 0:
            return GetAccommodationCostSerializer(cost_obj, many=True).data
        else:
            return []

    class Meta:
        model = SalesConfirmationAccommodation
        fields = "__all__"


class CreateSalesConfirmationAccommodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesConfirmationAccommodation
        fields = "__all__"


class UpdateSalesConfirmationAccommodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesConfirmationAccommodation
        fields = "__all__"


class GetAccommodationCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccommodationCost
        fields = "__all__"


class CreateAccommodationCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccommodationCost
        fields = "__all__"


class UpdateAccommodationCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccommodationCost
        fields = "__all__"


class GetSalesConfirmationChartersPriceListSerializer(serializers.ModelSerializer):
    charters_price_list = GetSalesChartersPriceListSerializer()

    class Meta:
        model = SalesConfirmationChartersPriceList
        fields = "__all__"


class CreateSalesConfirmationChartersPriceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesConfirmationChartersPriceList
        fields = "__all__"


class UpdateSalesConfirmationChartersPriceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesConfirmationChartersPriceList
        fields = "__all__"
