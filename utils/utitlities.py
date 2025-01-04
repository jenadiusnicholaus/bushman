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


# from django.utils import timezone
# from datetime import datetime, timedelta
# from your_app.models import Quota  # Replace 'your_app' with your actual app name


class CurrentQuota:
    from bm_hunting_settings.models import Quota

    current_date = timezone.now().date()

    # Fetch the current valid quota
    current_quota = None
    quotas = Quota.objects.all()

    try:
        for q in quotas:
            if q.end_date >= current_date:  # Check if the quota is still valid
                current_quota = q
                break

        # If no valid quota exists, create one
        if not current_quota:
            # Define the start and end dates for the new quota
            current_year = current_date.year
            start_date = datetime(current_year, 7, 1)  # July 1 of the current year
            end_date = datetime(current_year + 1, 6, 30)  # June 30 of the next year

            # Check if a quota for this period already exists
            existing_quota = Quota.objects.filter(
                start_date=start_date, end_date=end_date
            ).exists()

            if not existing_quota:
                # Create the new quota
                current_quota = Quota.objects.create(
                    start_date=start_date,
                    end_date=end_date,
                    name=f"Quota for {current_year}",
                )
                print(f"Created a new quota: {current_quota}")
            else:
                print("Quota for the next year already exists.")
        else:
            print(f"Current valid quota: {current_quota}")

    except Quota.DoesNotExist:
        CurrentQuota = None
