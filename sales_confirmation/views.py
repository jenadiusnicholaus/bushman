from rest_framework import viewsets

from sales_confirmation.models import SalesConfirmationProposal
from sales_confirmation.serializers import (
    CreateSalesConfirmationProposalAdditionalServiceSerializer,
    CreateSalesConfirmationProposalItinerarySerializer,
    CreateSalesConfirmationProposalPackageSerializer,
    CreateSalesConfirmationProposalSerializer,
    GetSalesConfirmationProposalSerializer,
)
from django.utils import timezone
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class SalesConfirmationViewSet(viewsets.ModelViewSet):
    serializer_class = GetSalesConfirmationProposalSerializer
    queryset = SalesConfirmationProposal.objects.all().order_by("-created_date")
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        confirmation_proposal_data = {
            "sales_inquiry": request.data.get("sales_inquiry_id"),
        }

        with transaction.atomic():
            proposal_serializer = CreateSalesConfirmationProposalSerializer(
                data=confirmation_proposal_data
            )
            if not proposal_serializer.is_valid():
                return Response(
                    {
                        "message": "Proposal creation failed",
                        "errors": proposal_serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            saved_proposal = proposal_serializer.save()

            package_name_data = {
                "sales_confirmation_proposal": saved_proposal.id,
                "package": request.data.get("package_id"),
            }
            package_serializer = CreateSalesConfirmationProposalPackageSerializer(
                data=package_name_data
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
                    {
                        "message": "Itinerary creation failed",
                        "errors": itinerary_serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            saved_itinerary = itinerary_serializer.save()

            # Handle multiple additional services
            # services = request.data.get("services", [])
            # for service_data in services:
            #     additional_service_data = {
            #         "sales_confirmation_proposal": saved_proposal.id,
            #         "service": service_data.get("service"),
            #         "quantity": service_data.get("quantity"),
            #         "price": service_data.get("price"),
            #     }
            #     additional_service_serializer = (
            #         CreateSalesConfirmationProposalAdditionalServiceSerializer(
            #             data=additional_service_data
            #         )
            #     )

            #     if not additional_service_serializer.is_valid():
            #         saved_proposal.delete()
            #         saved_package.delete()
            #         saved_itinerary.delete()
            #         return Response(
            #             {
            #                 "message": "Additional service creation failed",
            #                 "errors": additional_service_serializer.errors,
            #             },
            #             status=status.HTTP_400_BAD_REQUEST,
            #         )

            #     saved_additional_service = additional_service_serializer.save()

            return Response(
                {
                    "message": "Sales Confirmation Proposal Created",
                },
                status=status.HTTP_201_CREATED,
            )
