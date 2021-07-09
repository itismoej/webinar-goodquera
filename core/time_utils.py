from datetime import timedelta, datetime
from typing import Callable

from django.utils import timezone


def n_days_from_now(n: int) -> Callable[[int], datetime]:
    def func() -> datetime:
        return timezone.now() + timedelta(days=n)
    return func
