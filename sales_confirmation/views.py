from rest_framework import viewsets


from sales_confirmation.models import (
    SalesConfirmationAccommodation,
    SalesConfirmationProposal,
    SalesConfirmationProposalSafaryExtras,
    SalesConfirmationProposalStatus,
    SalesQuotaSpeciesStatus,
)
from sales_confirmation.serializers import (
    CreateAccommodationAddressSerializer,
    CreateAccommodationCostSerializer,
    CreateAccommodationTypeSerializer,
    CreateInstallmentSerializer,
    CreateSalesConfirmationAccommodationSerializer,
    CreateSalesConfirmationProposalItinerarySerializer,
    CreateSalesConfirmationProposalPackageSerializer,
    CreateSalesConfirmationProposalSafaryExtrasSerializer,
    CreateSalesConfirmationProposalSerializer,
    GetSalesConfirmationAccommodationSerializer,
    GetSalesConfirmationProposalSafaryExtrasSerializer,
    GetSalesConfirmationProposalSerializer,
    GetSalesConfirmationProposalStatusSerializer,
    GetSalesQuotaSpeciesStatusSerializer,
    UpdateSalesConfirmationProposalStatusSerializer,
    UploadDocSerializer,
)
from django.utils import timezone
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from utils.sales_price_breakdown import calculate_total_cost
from utils.track_species_status import TrackSpeciesStatus
from utils.pdf import SalesConfirmationPDF


class SalesConfirmationViewSet(viewsets.ModelViewSet):
    serializer_class = GetSalesConfirmationProposalSerializer
    queryset = SalesConfirmationProposal.objects.all().order_by("-created_date")
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        status_list = request.query_params.get("status_list", None)
        if status_list is not None:
            queryset = queryset.filter(status__status__in=status_list.split(","))
        serializer = self.get_serializer(queryset, many=True)
        response_data = []
        for data in serializer.data:
            #  def get_pdf(self, obj):
            pdf_file = SalesConfirmationPDF.generate_pdf(data, return_type="base64")
            data["pdf"] = pdf_file["pdf"]
            response_data.append(data)
        return Response(response_data)

        # return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        confirmation_proposal_data = {
            "sales_inquiry": request.data.get("sales_inquiry_id"),
            "regulatory_package": request.data.get("regulatory_package_id"),
        }

        # with transaction.atomic():
        proposal_serializer = CreateSalesConfirmationProposalSerializer(
            data=confirmation_proposal_data
        )
        if not proposal_serializer.is_valid():
            return Response(
                proposal_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        saved_proposal = proposal_serializer.save()

        bushman_package_data = {
            "sales_confirmation_proposal": saved_proposal.id,
            "package": request.data.get("package_id"),
        }
        package_serializer = CreateSalesConfirmationProposalPackageSerializer(
            data=bushman_package_data
        )

        if not package_serializer.is_valid():
            saved_proposal.delete()
            return Response(
                {
                    "message": "Package creation failed",
                    "errors": package_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        saved_package = package_serializer.save()

        itinerary_data = {
            "sales_confirmation_proposal": saved_proposal.id,
            "airport_name": request.data.get("airport_name"),
            "charter_in": request.data.get("charter_in"),
            "charter_out": request.data.get("charter_out"),
            "arrival": request.data.get("arrival"),
        }

        itinerary_serializer = CreateSalesConfirmationProposalItinerarySerializer(
            data=itinerary_data
        )

        if not itinerary_serializer.is_valid():
            saved_proposal.delete()
            saved_package.delete()
            return Response(
                itinerary_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        saved_itinerary = itinerary_serializer.save()

        installments = request.data.get("installments", [])
        for installment in installments:

            installment_data = {
                "sales_confirmation_proposal": saved_proposal.id,
                "narration": installment.get("narration"),
                "amount_due": installment.get("amount"),
                "amount_due_type": installment.get("amount_type"),
                "due_days": installment.get("days"),
                "due_days_type": installment.get("due_days_type"),
            }

            installment_serializer = CreateInstallmentSerializer(data=installment_data)

            if not installment_serializer.is_valid():
                saved_proposal.delete()
                saved_package.delete()
                saved_itinerary.delete()
                return Response(
                    installment_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )
            saved_installment = installment_serializer.save()

        return Response(
            {
                "message": "Sales Confirmation  Created",
                "data": proposal_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class CalculateTotalSalesAmount(APIView):
    def get(self, request, format=None):
        sales_inquiry_id = request.query_params.get("sales_inquiry_id")
        package_id = request.query_params.get("package_id")

        response_data = calculate_total_cost(
            sales_inquiry_id=sales_inquiry_id, package_id=package_id
        )
        return Response(response_data, status=status.HTTP_200_OK)


class SalesConfirmation(viewsets.ModelViewSet):
    serializer_class = GetSalesConfirmationProposalStatusSerializer
    queryset = SalesConfirmationProposalStatus.objects.filter().order_by("-created_at")
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        # we save signed document here use UploadDocSerializer
        # and update the status of proposal use CreateSalesConfirmationProposalStatusSerializer
        quota_id = request.data.get("quota_id")
        area_id = request.data.get("area_id")
        contract_doc = request.data.get("contract_doc")
        payment_doc = request.data.get("payment_doc")
        documents = []
        if contract_doc is not None and contract_doc != "undefined":
            documents.append({"type": "contract", "file": contract_doc})

        if payment_doc is not None and payment_doc != "undefined":
            documents.append({"type": "payment_receipt", "file": payment_doc})
        saved_doc = None
        if len(documents) > 0:
            for doc in documents:
                doc_data = {
                    "doc_type": doc.get("type"),
                    "entity": request.data.get("entity_id"),
                    "document": doc.get("file"),
                }
                doc_serializer = UploadDocSerializer(data=doc_data)
                if not doc_serializer.is_valid():
                    return Response(
                        doc_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                saved_doc = doc_serializer.save()

        status_obj, created = SalesConfirmationProposalStatus.objects.get_or_create(
            sales_confirmation_proposal_id=request.data.get(
                "sales_confirmation_proposal_id"
            )
        )

        status_data = {
            "user": request.user.id,
            "sales_confirmation_proposal": request.data.get(
                "sales_confirmation_proposal_id", status_obj.sales_confirmation_proposal
            ),
            "status": request.data.get("status_id", status_obj.status),
            "document": None,
            "created_at": timezone.now(),
        }
        try:

            TrackSpeciesStatus.track(
                request.data.get("sales_confirmation_proposal_id"),
                request.data.get("status_id"),
                area_id,
                status_obj,
            )
        except Exception as e:
            saved_doc.delete()
            return Response(
                {"message": f"{e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # status_data["document"] = saved_doc.id
        status_serializer = UpdateSalesConfirmationProposalStatusSerializer(
            instance=status_obj, data=status_data, partial=True
        )
        if not status_serializer.is_valid():
            return Response(
                status_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        saved_status = status_serializer.save()

        return Response(
            {
                "message": "Sales confirmation changed status",
                "data": status_serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class GetCalendaStats(viewsets.ModelViewSet):
    queryset = SalesQuotaSpeciesStatus.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = GetSalesQuotaSpeciesStatusSerializer


class SalesConfirmationProposalSafaryExtrasViewSets(viewsets.ModelViewSet):
    queryset = SalesConfirmationProposalSafaryExtras.objects.all()
    serializer_class = GetSalesConfirmationProposalSafaryExtrasSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        sales_inquiry_id = request.query_params.get("sales_inquiry_id")
        # get all huting areas
        querySet = self.get_queryset()

        if sales_inquiry_id is not None:
            querySet = querySet.filter(sales_inquiry__id=sales_inquiry_id)
        serializer = self.get_serializer(querySet, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):

        extras = request.data.get("safary_extras")
        if extras is None:
            return Response(
                {"message": "Safary extras is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        with transaction.atomic():
            for extra in extras:

                data = {
                    "safari_extras": extra.get("safari_extras_id"),
                    "sales_inquiry": extra.get("sales_inquiry_id"),
                    "account": extra.get("account_id"),
                }

                create_proposal_sz = (
                    CreateSalesConfirmationProposalSafaryExtrasSerializer(data=data)
                )
                if not create_proposal_sz.is_valid():
                    # delete all created proposal if any error occur

                    return Response(
                        create_proposal_sz.errors, status=status.HTTP_400_BAD_REQUEST
                    )

                proposal = create_proposal_sz.save()

            return Response(
                {"message": "Safari extras created successfully"},
                status=status.HTTP_201_CREATED,
            )


class SalesConfirmationAccommodationViewSets(viewsets.ModelViewSet):
    queryset = SalesConfirmationAccommodation.objects.all()
    serializer_class = GetSalesConfirmationAccommodationSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        sales_inquiry_id = request.query_params.get("sales_inquiry_id")
        # get all huting areas
        querySet = self.get_queryset()
        if sales_inquiry_id is not None:
            querySet = querySet.filter(sales_inquiry__id=sales_inquiry_id)
        serializer = self.get_serializer(querySet, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        sales_inquiry_id = request.data.get("sales_inquiry_id")

        type_data = {
            "name": request.data.get("type_name"),
        }

        address_data = {
            "street": request.data.get("address_street"),
            "city": request.data.get("address_city"),
            "zipcode": request.data.get("address_zipcode"),
        }

        accommodation_data = {
            "sales_inquiry": sales_inquiry_id,
            "entity": request.data.get("entity_id"),
            "type": None,
            "address": None,
            "booking_number": request.data.get("booking_number"),
            "check_in": request.data.get("check_in"),
            "check_out": request.data.get("check_out"),
        }

        cost_data = {
            "accommodation": None,
            "account": request.data.get("account_id"),
            "amount": request.data.get("amount"),
            "currency": request.data.get("currency"),
        }

        with transaction.atomic():
            type_serializer = CreateAccommodationTypeSerializer(data=type_data)
            if not type_serializer.is_valid():
                return Response(
                    type_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            type_obj = type_serializer.save()
            address_serializer = CreateAccommodationAddressSerializer(data=address_data)
            if not address_serializer.is_valid():
                type_obj.delete()
                return Response(
                    address_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            address_obj = address_serializer.save()
            accommodation_data["type"] = type_obj.id
            accommodation_data["address"] = address_obj.id
            accommodation_serializer = CreateSalesConfirmationAccommodationSerializer(
                data=accommodation_data
            )
            if not accommodation_serializer.is_valid():
                address_obj.delete()
                type_obj.delete()
                return Response(
                    accommodation_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            accommodation_obj = accommodation_serializer.save()
            cost_data["accommodation"] = accommodation_obj.id
            cost_serializer = CreateAccommodationCostSerializer(data=cost_data)
            if not cost_serializer.is_valid():
                accommodation_obj.delete()
                address_obj.delete()
                type_obj.delete()
                return Response(
                    cost_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            cost_obj = cost_serializer.save()
            return Response(
                {"message": "Accommodation created successfully"},
                status=status.HTTP_201_CREATED,
            )
