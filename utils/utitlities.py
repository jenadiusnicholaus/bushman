from datetime import datetime
from django.utils import timezone


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


class CurrentQuota:

    @staticmethod
    def get_current_quota():
        current_date = timezone.now().date()
        from bm_hunting_settings.models import Quota

        # Fetch currently valid quotas (those that have started and have not ended)
        current_quotas = Quota.objects.filter(
            start_date__lte=current_date, end_date__gte=current_date
        )

        if current_quotas.exists():
            current_quota = (
                current_quotas.first()
            )  # You can modify this to get the desired one if multiple exist
            print(f"Current valid quota: {current_quota}")
            return current_quota

        # If no current quota exists, check for future quotas
        future_quotas = Quota.objects.filter(start_date__gt=current_date)

        if future_quotas.exists():
            print("No current quota exists; the next quota starts in the future.")
            return None

        # If no valid or future quota exists, create a new quota for the next period
        current_year = current_date.year
        start_date = datetime(current_year, 7, 1).date()  # July 1 of the current year
        end_date = datetime(current_year + 1, 6, 30).date()  # June 30 of the next year

        # Check if a quota for this period already exists
        existing_quota = Quota.objects.filter(
            start_date=start_date, end_date=end_date
        ).exists()

        if not existing_quota:
            # Create the new quota
            new_quota = Quota.objects.create(
                start_date=start_date,
                end_date=end_date,
                name=f"Quota for {current_year}",
            )
            print(f"Created a new quota: {new_quota}")
            return new_quota
        else:
            print("Quota for the next year already exists.")
            return None


# Example usage:
# current_quota_instance = CurrentQuota.get_current_quota()
