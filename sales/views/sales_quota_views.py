from bm_hunting_settings.models import (
    HuntingArea,
    HuntingQuatasArea,
    Quota,
    QuotaHuntingAreaSpecies,
)
from sales.serializers.sales_inquiries_serializers import UpdateContactsSerializers
from sales.serializers.sales_quota_serializers import (
    GetQuotaSerializer,
    QuotaHuntingAreaSpeciesSerializers,
    CreateQuotaHuntingAreaSpeciesSerializers,
    CreateHuntingQuatasAreaSerializers,
)
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from utils.pdf import QuotaPDF


class QuotaViewSets(viewsets.ModelViewSet):
    serializer_class = GetQuotaSerializer
    queryset = Quota.objects.filter().order_by("-create_at")
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        quota_id = request.query_params.get("quota_id", None)
        quota_year = request.query_params.get("year", None)
        quota_species = request.query_params.get("species", None)

        if quota_id:
            try:
                ob = Quota.objects.get(id=quota_id)
                serializer = self.get_serializer(ob)
                return Response(serializer.data)
            except Quota.DoesNotExist:
                return Response({"error": "Quota not found"}, status=404)

        serializer = self.get_serializer(self.get_queryset().order_by("id"), many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):

        data = {
            "user": request.user.id,
            "name": request.data.get("name"),
            "description": request.data.get("description"),
            "start_date": request.data.get("start_date"),
            "end_date": request.data.get("end_date"),
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "Quota created successfully", "data": serializer.data},
            status=201,
        )

    def patch(self, request, *args, **kwargs):
        quota_id = request.query_params.get("quota_id", None)
        if not quota_id:
            return Response({"error": "Quota id not found"}, status=400)
        try:
            queryset = Quota.objects.get(id=quota_id)
        except Quota.DoesNotExist:
            return Response({"error": "Quota not found"}, status=404)
        serializer = self.get_serializer(queryset, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {
                "message": "Quota updated successfully",
                "data": serializer.data,
            }
        )

    def delete(self, request, *args, **kwargs):
        quota_id = request.query_params.get("quota_id", None)
        if not quota_id:
            return Response({"error": "Quota id not found"}, status=400)
        try:
            queryset = Quota.objects.get(id=quota_id)
        except Quota.DoesNotExist:
            return Response({"error": "Quota not found"}, status=404)
        self.perform_destroy(queryset)
        return Response({"message": "Quota deleted successfully"}, status=200)


class QuotaHuntingAreaSpeciesViewSets(viewsets.ModelViewSet):
    queryset = QuotaHuntingAreaSpecies.objects.all()
    serializer_class = QuotaHuntingAreaSpeciesSerializers
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):

        current_year = timezone.now().year
        quota_id = request.query_params.get("quota_id")
        species_id = request.query_params.get("species_id")
        area_id = request.query_params.get("area_id")

        # Initialize the queryset with all species
        querySet = self.get_queryset()

        # Handle 'null' strings and convert them to None
        if quota_id == "null":
            quota_id = None
        if species_id == "null":
            species_id = None
        if area_id == "null":
            area_id = None

        current_quota = None

        # If no filtering criteria are provided, filter for quotas that start in the current year
        if not quota_id and not species_id and not area_id:
            querySet = querySet.filter(quota__start_date__year=current_year)
            current_quota = Quota.objects.filter(start_date__year=current_year).first()

        # Filter the queryset based on the provided parameters
        if quota_id not in [None, ""]:
            querySet = querySet.filter(quota_id=quota_id)
            current_quota = Quota.objects.get(id=quota_id)

        if species_id not in [None, ""] and species_id != "all":
            querySet = querySet.filter(species_id=species_id)

        if area_id not in [None, ""]:
            querySet = querySet.filter(area_id=area_id)

        # Serialize the resulting queryset
        serializer = self.get_serializer(querySet, many=True)
        # generated_pdf = Q
        pdf_title = (
            f"Quota report for {current_quota.name}, Start: {current_quota.start_date} End: {current_quota.end_date}"
            if current_quota
            else "Quota"
        )
        pdf_response = QuotaPDF.generate_pdf(
            serializer.data, return_type="base64", title=pdf_title
        )

        # Combine your response data
        response_data = {
            "data": serializer.data,
            "pdf": pdf_response["pdf"],
        }

        return Response(response_data)

    def create(self, request, *args, **kwargs):
        # Prepare data for associated entities
        area_id = request.data.get("area_id")
        quota_id = request.data.get("quota_id")
        species_objects = request.data.get("species_objects", [])

        # Check for required fields
        if not area_id or not quota_id or not species_objects:
            return Response(
                {"error": "area_id, quota_id, and species_objects are required."},
                status=400,
            )

        hunting_area_data = {"area": area_id, "quota": quota_id}
        species_data_list = []

        # Begin transaction
        with transaction.atomic():
            # Prepare species data
            for obj in species_objects:
                if not obj.get("id") or not obj.get("quantity"):
                    return Response(
                        {
                            "error": "Each species object must have an 'id' and 'quantity'."
                        },
                        status=400,
                    )
                species_data_list.append(
                    {
                        "species": obj["id"],  # Access species id
                        "quota": quota_id,
                        "area": area_id,
                        "quantity": obj["quantity"],  # Access quantity
                    }
                )

            # quota_areas, created = HuntingQuatasArea.objects.get_or_create(
            #     area_id=area_id, quota_id=quota_id
            # )

            # Serialize hunting area
            # area_sz = CreateHuntingQuatasAreaSerializers(data=hunting_area_data)
            # if not area_sz.is_valid():
            #     return Response(area_sz.errors, status=400)

            # Save the area and handle potential database issues
            # area_instance = area_sz.save()

            # Validate and save each species
            for species_data in species_data_list:
                species_sz = CreateQuotaHuntingAreaSpeciesSerializers(data=species_data)
                if not species_sz.is_valid():
                    # area_instance.delete()  # Rollback area save if species fails
                    return Response(species_sz.errors, status=400)
                species_sz.save()

            return Response(
                {
                    "message": "Quota Hunting Area Species created successfully",
                    "data": species_data_list,
                },
                status=201,
            )
