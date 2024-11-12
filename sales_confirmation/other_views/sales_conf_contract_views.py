from bm_hunting_settings.serializers import (
    CreateGeoLocationsSerializers,
    CreateLocationSerializer,
)
from sales_confirmation.models import (
    EntityContractPermit,
    GameActivity,
    SalesConfirmationContract,
)
from sales_confirmation.serializers import (
    CreateEntityContactPermitDatesCreateSerializer,
    CreateEntityContractPermitSerializer,
    CreateGameActivityProfessionalHunterSerializer,
    CreateGameActivitySerializer,
    CreateGameKilledActivitySerializer,
    CreateSalesConfirmationContractSerializer,
    GetEntityContactPermitDatesSerializer,
    GetEntityContractPermitSerializer,
    GetGameActivitySerializer,
    GetSalesConfirmationContractSerializer,
)
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from utils.pdf import SalesContractPDF, PermitPDF, GamePDF
from rest_framework.permissions import IsAuthenticated
from django.db import transaction


class SalesConfirmationContractviewSet(viewsets.ModelViewSet):
    queryset = SalesConfirmationContract.objects.all()
    serializer_class = GetSalesConfirmationContractSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = []
        for data in serializer.data:
            pdf_file = SalesContractPDF.generate_pdf(data, return_type="base64")
            data["pdf"] = pdf_file["pdf"]
            response_data.append(data)
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        contract_data = {
            "sales_confirmation_proposal": request.data.get(
                "sales_confirmation_proposal_id"
            ),
            "entity": request.data.get("entity_id"),
            "start_date": request.data.get("start_date"),
            "end_date": request.data.get("end_date"),
            "description": request.data.get("description"),
        }
        serializer = CreateSalesConfirmationContractSerializer(data=contract_data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(
            {"message": "Contract created successfully", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )


class EntityContractPermitViewset(viewsets.ModelViewSet):
    queryset = EntityContractPermit.objects.all()
    serializer_class = GetEntityContractPermitSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = []
        for data in serializer.data:
            pdf_file = PermitPDF.generate_pdf(data, return_type="base64")
            data["pdf"] = pdf_file["pdf"]
            response_data.append(data)
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        # Prepare data for the permission and its contact dates
        permit_data = {
            "enity_contract": request.data.get("enity_contract_id"),
            "permit_number": request.data.get("permit_number"),
            "issued_date": request.data.get("issued_date"),
            "package_type": request.data.get("package_type"),
            "description": request.data.get("description"),
        }

        permit_dates_data = {
            "entity_contract_permit": None,  # This will be set later
            "start_date": request.data.get("start_date"),
            "end_date": request.data.get("end_date"),
            "amendment": request.data.get("amendment"),
        }

        # Start a database transaction
        with transaction.atomic():
            # 1. Validate and save the contract permit
            permit_serializer = CreateEntityContractPermitSerializer(data=permit_data)
            if not permit_serializer.is_valid():
                return Response(
                    permit_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            # Save permitted object
            saved_permit_obj = permit_serializer.save()

            # 2. Prepare data for the contact dates and validate
            permit_dates_data["entity_contract_permit"] = (
                saved_permit_obj.id
            )  # Set the FK to the saved permit

            permit_dates_serializer = CreateEntityContactPermitDatesCreateSerializer(
                data=permit_dates_data
            )
            if not permit_dates_serializer.is_valid():
                saved_permit_obj.delete()  # Rollback saved permit object
                return Response(
                    permit_dates_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            # 3. Save the contact dates
            permit_dates_serializer.save()

        return Response(
            {
                "message": "Contract created successfully",
                "data": permit_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class GameActivityViewset(viewsets.ModelViewSet):
    queryset = GameActivity.objects.all()
    serializer_class = GetGameActivitySerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = []
        for data in serializer.data:
            pdf_file = GamePDF.generate_pdf(data, return_type="base64")
            data["pdf"] = pdf_file["pdf"]
            response_data.append(data)

        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        # Prepare data for game activity, geo location, location, and game killed activity
        game_activity_data = {
            "entity_contract_permit": request.data.get("entity_contract_permit_id"),
            "client": request.data.get("client_id"),
            "start_date": request.data.get("start_date"),
            "end_date": request.data.get("end_date"),
        }
        geo_location_data = {
            "coordinates_type": request.data.get("coordinates_type"),
            "coordinates": request.data.get("coordinates"),
        }
        location_data = {
            "location_type": request.data.get("location_type", None),
            "geo_coordinates": None,
            "is_disabled": request.data.get("is_disabled", False),
        }
        game_killed_activity_data = {
            "game_killed_registration": None,
            "species": request.data.get("species_id"),
            "quantity": request.data.get("quantity"),
            "location": None,
            "description": request.data.get("description"),
            "user": request.user.id,
            "spacies_gender": request.data.get("spacies_gender"),
            "status": request.data.get("status"),
        }
        # game_activity_professional_hunter_data = {
        #     "game_activity": None,  # To be set later
        #     "professional_hunter": request.data.get("professional_hunter_id"),
        #     "ph": request.data.get("ph_id"),
        # }

        # Use transaction.atomic() to manage rollback on failure
        with transaction.atomic():
            # 1. Validate and save the game activity
            game_activity_serializer = CreateGameActivitySerializer(
                data=game_activity_data
            )
            if not game_activity_serializer.is_valid():
                return Response(
                    game_activity_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            saved_game_activity_obj = game_activity_serializer.save()

            # 2. Validate and save the geo location
            geo_location_serializer = CreateGeoLocationsSerializers(
                data=geo_location_data
            )
            if not geo_location_serializer.is_valid():
                saved_game_activity_obj.delete()  # Rollback saved game activity object
                return Response(
                    geo_location_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            saved_geo_location_obj = geo_location_serializer.save()

            # 3. Validate and save the location
            location_data["geo_coordinates"] = saved_geo_location_obj.id
            location_serializer = CreateLocationSerializer(data=location_data)
            if not location_serializer.is_valid():
                saved_game_activity_obj.delete()
                saved_geo_location_obj.delete()
                return Response(
                    location_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            saved_location_obj = location_serializer.save()

            # 4. Validate and save the game killed activity
            game_killed_activity_data["location"] = saved_location_obj.id
            game_killed_activity_data["game_killed_registration"] = (
                saved_game_activity_obj.id
            )
            game_killed_activity_serializer = CreateGameKilledActivitySerializer(
                data=game_killed_activity_data
            )
            if not game_killed_activity_serializer.is_valid():
                saved_game_activity_obj.delete()
                saved_geo_location_obj.delete()
                saved_location_obj.delete()
                return Response(
                    game_killed_activity_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            saved_game_killed_activity_obj = game_killed_activity_serializer.save()

            # 5. Validate and save the game activity professional hunter
            # is possible to have multiple professional hunters for a game activity

            professional_hunters_ids = request.data.get("professional_hunters_ids")
            if professional_hunters_ids:
                for ph_id in professional_hunters_ids:
                    game_activity_professional_hunter_data = {
                        "game_activity": saved_game_activity_obj.id,
                        "ph": ph_id,
                    }
                    game_activity_professional_hunter_serializer = (
                        CreateGameActivityProfessionalHunterSerializer(
                            data=game_activity_professional_hunter_data
                        )
                    )
                    if not game_activity_professional_hunter_serializer.is_valid():
                        saved_game_activity_obj.delete()
                        saved_geo_location_obj.delete()
                        saved_location_obj.delete()
                        saved_game_killed_activity_obj.delete()
                        return Response(
                            game_activity_professional_hunter_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                    saved_game_activity_professional_hunter_obj = (
                        game_activity_professional_hunter_serializer.save()
                    )
                    # 6. Return the saved game activity data
                    return Response(
                        {
                            "message": "Game activity created successfully",
                            "data": game_activity_serializer.data,
                        },
                        status=status.HTTP_201_CREATED,
                    )

        return Response(
            {
                "message": "Game activity created successfully",
                "data": game_activity_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )