from rest_framework.response import Response
from rest_framework import status

from bm_hunting_settings.models import (
    HuntingPackageCompanionsHunter,
    HuntingPackageOberverHunter,
    HuntingPriceTypePackage,
)
from sales.models import SalesIquiryPreference


def calculate_total_cost(sales_inquiry_id, package_id):
    # sales_inquiry_id = request.query_params.get("sales_inquiry_id")
    # package_id = request.query_params.get("package_id")

    if not sales_inquiry_id or not package_id:
        return Response(
            {"message": "Missing sales_inquiry_id or package_id"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        sales_inquiry = SalesIquiryPreference.objects.get(
            sales_inquiry__id=sales_inquiry_id
        )
    except SalesIquiryPreference.DoesNotExist:
        return Response(
            {"message": "Sales Inquiry not found"}, status=status.HTTP_404_NOT_FOUND
        )

    try:
        package = HuntingPriceTypePackage.objects.get(sales_package__id=package_id)
    except HuntingPriceTypePackage.DoesNotExist:
        return Response(
            {"message": "Package not found"}, status=status.HTTP_404_NOT_FOUND
        )

    total_amount = package.price_list_type.amount
    currency = {
        "code": package.price_list_type.currency.name,
        "symbol": package.price_list_type.currency.symbol,
    }
    number_of_companions = sales_inquiry.no_of_companions
    number_of_observers = sales_inquiry.no_of_observers
    companion_cost = 0
    observer_cost = 0

    # Companion cost
    try:
        companion_cost_instance = HuntingPackageCompanionsHunter.objects.filter(
            hunting_price_list_type_package__id=package.id
        ).first()
        companion_cost = companion_cost_instance.amount
    except HuntingPackageCompanionsHunter.DoesNotExist:
        companion_cost = 0

    # Observer cost
    try:
        observer_cost_instance = HuntingPackageOberverHunter.objects.get(
            hunting_price_list_type_package__id=package.id
        )
        observer_cost = observer_cost_instance.amount
    except HuntingPackageOberverHunter.DoesNotExist:
        observer_cost = 0

    # Prepare response data
    companion_cost_detail = {}
    observer_cost_detail = {}

    if number_of_companions > 0:
        total_companion_cost = number_of_companions * companion_cost
        companion_cost_detail = {
            "number_of_companions": number_of_companions,
            "cost_per_companion": {"amount": companion_cost, "currency": currency},
            "total_companion_cost": {
                "amount": total_companion_cost,
                "currency": currency,
            },
        }
        total_amount += total_companion_cost

    if number_of_observers > 0:
        total_observer_cost = number_of_observers * observer_cost
        observer_cost_detail = {
            "number_of_observers": number_of_observers,
            "cost_per_observer": {"amount": observer_cost, "currency": currency},
            "total_observer_cost": {
                "amount": total_observer_cost,
                "currency": currency,
            },
        }
        total_amount += total_observer_cost

    response_data = {
        "total_amount": {"amount": total_amount, "currency": currency},
        "companion_cost_details": companion_cost_detail,
        "observer_cost_details": observer_cost_detail,
    }

    return response_data
