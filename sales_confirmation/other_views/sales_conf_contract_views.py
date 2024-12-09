from bm_hunting_settings.serializers import (
    CreateGeoLocationsSerializers,
    CreateLocationSerializer,
)
from sales.models import Entity
from sales_confirmation.models import (
    EntityContractPermit,
    GameActivity,
    GameKilledActivity,
    SalesConfirmationContract,
    SalesConfirmationProposal,
)
from sales_confirmation.serializers import (
    CreateEntityContractPermitDatesCreateSerializer,
    CreateEntityContractPermitSerializer,
    CreateGameActivityProfessionalHunterSerializer,
    CreateGameActivitySerializer,
    CreateGameKilledActivitySerializer,
    CreateSalesConfirmationContractSerializer,
    GetEntityContractPermitDatesSerializer,
    GetEntityContractPermitSerializer,
    GetGameActivitySerializer,
    GetGameKilledActivitySerializer,
    GetSalesConfirmationContractSerializer,
)
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from utils.pdf import SalesContractPDF, PermitPDF, GamePDF
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from rest_framework import generics

from utils.track_species_status import TrackSpeciesStatus


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
            "entity_contract": request.data.get("entity_contract_id"),
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
            permit_dates_data["entity_contract_permit"] = saved_permit_obj.id

            permit_dates_serializer = CreateEntityContractPermitDatesCreateSerializer(
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


#  to rethink this viewset
class ClientGameActivityViewset(viewsets.ModelViewSet):
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
            "area": request.data.get("area_id"),
            "time": request.data.get("time"),
            "date": request.data.get("date"),
            "weapon_used": request.data.get("weapon_used"),
            "description": request.data.get("description"),
            "user": request.user.id,
            "spacies_gender": request.data.get("spacies_gender"),
            "status": request.data.get("status"),
        }

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

    #


# to rethink this viewset
class GameActivityRegistrationForWebPlatFormvieSet(viewsets.ModelViewSet):
    queryset = GameActivity.objects.all()
    serializer_class = GetGameActivitySerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        game_activity_data = {
            "entity_contract_permit": request.data.get("entity_contract_permit_id"),
            "client": request.data.get("client_id"),
            "start_date": request.data.get("start_date"),
            "end_date": request.data.get("end_date"),
        }
        games = request.data.get("games")

        with transaction.atomic():

            # save client data first
            # game_activity_serializer = CreateGameActivitySerializer(
            #     data=game_activity_data
            # )
            # if not game_activity_serializer.is_valid():
            #     return Response(
            #         game_activity_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            #     )
            try:
                permit_instance = EntityContractPermit.objects.get(
                    id=request.data.get("entity_contract_permit_id")
                )
            except EntityContractPermit.DoesNotExist:
                return Response(
                    {"message": "Entity contract permit not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            try:
                client_instance = Entity.objects.get(id=request.data.get("client_id"))
            except permit_instance.client.model.DoesNotExist:
                return Response(
                    {"message": "Client not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            # if GameActivity.objects.filter(
            #     entity_contract_permit=permit_instance,
            #     client=client_instance,
            # ).exists():
            #     return Response(
            #         {"message": "Game activity already exists for this client"},
            #         status=status.HTTP_400_BAD_REQUEST,
            #     )

            game_activity, activity_created = GameActivity.objects.get_or_create(
                entity_contract_permit=permit_instance,
                client=client_instance,
                defaults={
                    "entity_contract_permit": permit_instance,
                    "client": client_instance,
                    "start_date": request.data.get("start_date"),
                    "end_date": request.data.get("end_date"),
                    "status": "INITIATED",
                },
            )
            if not activity_created or request.data.get("game_state") is not None:
                game_activity.status = request.data.get("game_state")
                game_activity.save()

            saved_game_activity_obj = game_activity

            if len(games) > 0:
                for game in games:
                    geo_location_data = {
                        "coordinates_type": game.get("coordinates_type"),
                        "coordinates": game.get("coordinates"),
                    }
                    location_data = {
                        "location_type": game.get("location_type", None),
                        "geo_coordinates": None,
                        "is_disabled": game.get("is_disabled", False),
                    }
                    game_killed_activity_data = {
                        "game_killed_registration": None,
                        "species": game.get("species_id"),
                        "quantity": game.get("quantity"),
                        "location": None,
                        "area": game.get("area_id"),
                        "time": game.get("time"),
                        "date": game.get("date"),
                        "weapon_used": game.get("weapon_used"),
                        "description": game.get("description"),
                        "user": request.user.id,
                        "spacies_gender": game.get("spacies_gender"),
                        "status": game.get("status"),
                    }

                    # 2. Validate and save the geo location
                    geo_location_serializer = CreateGeoLocationsSerializers(
                        data=geo_location_data
                    )
                    if not geo_location_serializer.is_valid():
                        # delete game activity if geo location is not valid
                        saved_game_activity_obj.delete()
                        return Response(
                            geo_location_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                    saved_geo_location_obj = geo_location_serializer.save()
                    # 3. Validate and save the location
                    location_data["geo_coordinates"] = saved_geo_location_obj.id
                    location_serializer = CreateLocationSerializer(data=location_data)
                    if not location_serializer.is_valid():
                        # delete game activity and geo location if location is not valid
                        saved_game_activity_obj.delete()
                        saved_geo_location_obj.delete()

                        return Response(
                            location_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                    saved_location_obj = location_serializer.save()
                    # 4. Validate and save the game killed activity
                    game_killed_activity_data["location"] = saved_location_obj.id
                    game_killed_activity_data["game_killed_registration"] = (
                        saved_game_activity_obj.id
                    )
                    game_killed_activity_serializer = (
                        CreateGameKilledActivitySerializer(
                            data=game_killed_activity_data
                        )
                    )
                    if not game_killed_activity_serializer.is_valid():
                        # delete game activity, geo location, and location if game killed activity is not valid
                        saved_game_activity_obj.delete()
                        saved_geo_location_obj.delete()
                        saved_location_obj.delete()
                        return Response(
                            game_killed_activity_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                    try:
                        TrackSpeciesStatus.trackTakenOrSoldSpecies(
                            sales_confirmation_proposal_id=game_activity.entity_contract_permit.entity_contract.sales_confirmation_proposal.id,
                            status="completed",
                            area_id=game.get("area_id"),
                            species_id=game.get("species_id"),
                            teken_quantity=game.get("quantity"),
                            game_state=request.data.get("game_state"),
                        )
                        saved_game_killed_activity_obj = (
                            game_killed_activity_serializer.save()
                        )
                    except Exception as e:
                        return Response(
                            {"message": f"{e}"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

            professional_hunters_ids = request.data.get("professional_hunters_ids")
            if len(professional_hunters_ids) > 0 and activity_created:
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
                        },
                        status=status.HTTP_201_CREATED,
                    )

        return Response(
            {
                "message": "Game activity created successfully",
            },
            status=status.HTTP_201_CREATED,
        )


class InitiateClientGameViewSet(generics.CreateAPIView):
    queryset = GameActivity.objects.all()
    serializer_class = GetGameActivitySerializer
    permission_classes = [IsAuthenticated]
    allowed_methods = "POST"

    def create(self, request, *args, **kwargs):
        game_activity_data = {
            "entity_contract_permit": request.data.get("entity_contract_permit_id"),
            "client": request.data.get("client_id"),
            "status": "INITIATED",
            "start_date": request.data.get("start_date"),
            "end_date": request.data.get("end_date"),
        }
        professional_hunters_ids = request.data.get("professional_hunters_ids")

        with transaction.atomic():
            # save client data first
            game_activity_serializer = CreateGameActivitySerializer(
                data=game_activity_data
            )
            if not game_activity_serializer.is_valid():
                return Response(
                    game_activity_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            saved_game_activity_obj = game_activity_serializer.save()

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

                        return Response(
                            game_activity_professional_hunter_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                    saved_game_activity_professional_hunter_obj = (
                        game_activity_professional_hunter_serializer.save()
                    )

            return Response(
                {
                    "message": "Game activity created successfully",
                    "data": game_activity_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )


class GameActivitiesViewSet(viewsets.ModelViewSet):

    queryset = GameKilledActivity.objects.all()
    serializer_class = GetGameKilledActivitySerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        game_activity_id = self.request.query_params.get("game_activity_id")
        if game_activity_id:
            queryset = self.get_queryset().filter(
                game_killed_registration=game_activity_id
            )
        else:
            queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):

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
            "game_killed_registration": request.data.get("game_activity_id"),
            "species": request.data.get("species_id"),
            "quantity": request.data.get("quantity"),
            "location": None,
            "area": request.data.get("area_id"),
            "time": request.data.get("time"),
            "date": request.data.get("date"),
            "weapon_used": request.data.get("weapon_used"),
            "description": request.data.get("description"),
            "user": request.user.id,
            "spacies_gender": request.data.get("spacies_gender"),
            "status": request.data.get("status"),
        }

        # Use transaction.atomic() to manage rollback on failure
        with transaction.atomic():
            # 1. Validate and save the geo location
            geo_location_serializer = CreateGeoLocationsSerializers(
                data=geo_location_data
            )
            if not geo_location_serializer.is_valid():
                return Response(
                    geo_location_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
            saved_geo_location_obj = geo_location_serializer.save()
            # 2. Validate and save the location
            location_data["geo_coordinates"] = saved_geo_location_obj.id
            location_serializer = CreateLocationSerializer(data=location_data)
            if not location_serializer.is_valid():
                saved_geo_location_obj.delete()
                return Response(
                    location_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
            saved_location_obj = location_serializer.save()

            # 3. Validate and save the game killed activity
            game_killed_activity_data["location"] = saved_location_obj.id
            game_killed_activity_serializer = CreateGameKilledActivitySerializer(
                data=game_killed_activity_data
            )
            if not game_killed_activity_serializer.is_valid():
                saved_location_obj.delete()
                saved_geo_location_obj.delete()
                return Response(
                    game_killed_activity_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:

                TrackSpeciesStatus.trackTakenOrSoldSpecies(
                    sales_confirmation_proposal_id=request.data.get(
                        "sales_confirmation_proposal_id"
                    ),
                    status="completed",
                    area_id=request.data.get("area_id"),
                    species_id=request.data.get("species_id"),
                    teken_quantity=request.data.get("quantity"),
                    game_state=request.data.get("game_state"),
                )
                saved_game_killed_activity_obj = game_killed_activity_serializer.save()

            except Exception as e:
                return Response(
                    {"message": f"{e}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # 4. Return the saved game killed activity data
            return Response(
                {
                    "message": "Game killed activity created successfully",
                    "data": game_killed_activity_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
