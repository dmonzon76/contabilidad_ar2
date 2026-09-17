from datetime import date
from accounting.models import Period


class NoOpenPeriodError(Exception):
    pass


def get_open_period_for_date(operation_date: date):
    """
    Returns the open accounting period for the given date.
    Raises NoOpenPeriodError if none exists.
    """

    period = Period.objects.filter(
        start_date__lte=operation_date,
        end_date__gte=operation_date,
        status="OPEN",
    ).first()

    if not period:
        raise NoOpenPeriodError(
            f"No hay un período contable abierto para la fecha {operation_date.isoformat()}."
        )

    return period
