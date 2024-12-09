from datetime import datetime
from django.utils import timezone

from bm_hunting_settings.models import Quota


def format_any_date(date):
    """
    Convert any date input to a timezone-aware datetime object or a string in the format YYYY-MM-DD.

    Args:
        date (str, datetime, or None): The date to be formatted.

    Returns:
        datetime: A timezone-aware datetime object.

    Raises:
        ValueError: If the input date is in an incorrect format.
    """

    # Handle if the incoming date is None
    if date is None:
        raise ValueError("No date provided")

    # Check the type of date input
    if isinstance(date, str):
        # Attempt to parse string date formats
        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y"):
            try:
                # Try to parse it with different formats
                parsed_date = datetime.strptime(date, fmt)
                # Make sure parsed_date is timezone-aware
                if parsed_date.tzinfo is None:
                    parsed_date = timezone.make_aware(
                        parsed_date
                    )  # Convert to UTC or local timezone
                return parsed_date  # Return as a timezone-aware datetime
            except ValueError:
                continue
        raise ValueError(
            "Incorrect date format, should be YYYY-MM-DD or other recognized formats"
        )

    elif isinstance(date, datetime):
        # If it's a timezone-aware datetime object, return it directly
        if date.tzinfo is None:
            date = timezone.make_aware(date)  # Make naive datetime timezone-aware
        return date  # Return as a timezone-aware datetime

    else:
        raise ValueError("Unsupported date type. Must be a string or datetime object.")


class currentQuuta:
    current_year = timezone.now().year
    current_quota = Quota.objects.filter(start_date__year=current_year).first()
