from bm_hunting_settings.models import Quota
from sales.serializers.sales_quota_serializers import GetQuotaSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class QuotaViewSets(viewsets.ModelViewSet):
    serializer_class = GetQuotaSerializer
    queryset = Quota.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        quota_id = request.query_params.get("quota_id", None)
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "Quota created successfully", "data": serializer.data},
            status=201,
            headers=headers,
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
