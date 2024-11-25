from rest_framework import viewsets


from sales_confirmation.models import (
    SalesConfirmationProposal,
    SalesConfirmationProposalStatus,
    SalesQuotaSpeciesStatus,
)
from sales_confirmation.serializers import (
    CreateInstallmentSerializer,
    CreateSalesConfirmationProposalItinerarySerializer,
    CreateSalesConfirmationProposalPackageSerializer,
    CreateSalesConfirmationProposalSerializer,
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
        if status_list:
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
                "message": "Sales Confirmation Proposal Created",
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

        TrackSpeciesStatus.track(
            request.data.get("sales_confirmation_proposal_id"),
            request.data.get("status_id"),
            # quota_id,
            area_id,
            status_obj,
        )

        # status_data["document"] = saved_doc.id
        status_serializer = UpdateSalesConfirmationProposalStatusSerializer(
            instance=status_obj, data=status_data, partial=True
        )
        if not status_serializer.is_valid():
            # saved_doc.delete()
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
