from rest_framework import filters
from .models import SalesInquiry


class MetricFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter()

    class Meta:
        model = SalesInquiry
        fields = ['season', 'create_date', 'sales_inquiry_preference_set__prefferred_date',"code"]