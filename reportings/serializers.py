from rest_framework import serializers

from bm_hunting_settings.models import Quota, QuotaHuntingAreaSpecies
from sales_confirmation.models import SalesQuotaSpeciesStatus


class GetQuotaStatsSerializer(serializers.ModelSerializer):
    # SalesQuotaSpeciesStatus
    confirmed = serializers.SerializerMethodField()
    pending = serializers.SerializerMethodField()
    cancelled = serializers.SerializerMethodField()
    taken = serializers.SerializerMethodField()
    provisoned = serializers.SerializerMethodField()
    # total_qouta_sales = serializers.SerializerMethodField()
    total_quota_balance = serializers.SerializerMethodField()

    # SalesQuotaSpeciesStatus
    class Meta:
        model = Quota
        fields = "__all__"

    #
    def count_species_status(self, status, obj):
        status = SalesQuotaSpeciesStatus.objects.filter(status=status, quota=obj)
        return sum(status.values_list("quantity", flat=True))

    def get_confirmed(self, obj):
        return self.count_species_status("confirmed", obj)

    def get_pending(self, obj):
        return self.count_species_status("pending", obj)

    def get_cancelled(self, obj):
        return self.count_species_status("cancelled", obj)

    def get_taken(self, obj):
        return self.count_species_status("completed", obj)

    def get_provisoned(self, obj):
        return self.count_species_status("provision_sales", obj)

    def get_total_quota_balance(self, obj):
        qas = QuotaHuntingAreaSpecies.objects.filter(quota=obj)
        return sum(qas.values_list("quantity", flat=True))
