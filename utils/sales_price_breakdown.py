from rest_framework.response import Response
from rest_framework import status

from bm_hunting_settings.models import (
    HuntingPackageCompanionsHunter,
    HuntingPackageOberverHunter,
    HuntingPriceTypePackage,
)
from sales.models import SalesIquiryPreference

from rest_framework.exceptions import NotFound, ValidationError


from rest_framework.exceptions import NotFound, ValidationError


def calculate_total_cost(sales_inquiry_id, package_id):
    if not sales_inquiry_id or not package_id:
        raise ValidationError({"message": "Missing sales_inquiry_id or package_id"})

    try:
        sales_inquiry = SalesIquiryPreference.objects.get(
            sales_inquiry__id=sales_inquiry_id
        )
    except SalesIquiryPreference.DoesNotExist:
        raise NotFound({"message": "Sales Inquiry not found"})
    except Exception as e:
        raise ValidationError({"message": str(e)})

    package = HuntingPriceTypePackage.objects.filter(
        sales_package__id=package_id
    ).first()
    if package is None:
        raise NotFound({"message": "Package not found"})

    if package.price_list_type is None:
        raise ValidationError({"message": "Price list type not found"})

    total_amount = (
        package.price_list_type.amount
        if package.price_list_type.amount is not None
        else 0
    )

    # Check for valid currency data
    if package.price_list_type.currency is None:
        raise ValidationError({"message": "Currency not found"})

    currency = {
        "code": package.price_list_type.currency.name,
        "symbol": package.price_list_type.currency.symbol,
    }

    # Validate numbers of companions and observers
    number_of_companions = sales_inquiry.no_of_companions
    number_of_observers = sales_inquiry.no_of_observers

    if not isinstance(number_of_companions, int) or number_of_companions < 0:
        raise ValidationError({"message": "Invalid number of companions"})
    if not isinstance(number_of_observers, int) or number_of_observers < 0:
        raise ValidationError({"message": "Invalid number of observers"})

    companion_cost = 0
    observer_cost = 0

    # Companion cost
    companion_cost_instance = HuntingPackageCompanionsHunter.objects.filter(
        hunting_price_list_type_package__id=package.id
    ).first()
    if companion_cost_instance and companion_cost_instance.amount is not None:
        companion_cost = companion_cost_instance.amount
    else:
        pass

    # Observer cost
    observer_cost_instance = HuntingPackageOberverHunter.objects.filter(
        hunting_price_list_type_package__id=package.id
    ).first()
    if observer_cost_instance and observer_cost_instance.amount is not None:
        observer_cost = observer_cost_instance.amount
    else:
        pass

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
