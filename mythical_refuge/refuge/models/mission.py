from decimal import Decimal
from dataclasses import dataclass, field
from datetime import date, timedelta

from refuge.exceptions import ValidationError


@dataclass(eq=False)
class Mission:
    creature_name: str
    handler_name: str
    destination: str
    departure_date: date
    duration_days: int
    base_reward: Decimal
    danger_multiplier: Decimal = Decimal("1.0")
    returned_on: date | None = None
    notes: str = ""
    id: int | None = field(default=None, repr=False)

    def __post_init__(self):
        if not self.destination:
            raise ValidationError("destination cannot be empty.")
        if self.duration_days <= 0:
            raise ValidationError(
                f"duration_days must be a strictly positive integer, got {self.duration_days}."
            )

        self.base_reward = Decimal(str(self.base_reward))

        if self.base_reward < 0:
            raise ValidationError("base_reward must be positive.")

        self.danger_multiplier = Decimal(str(self.danger_multiplier))

    @property
    def due_date(self) -> date:
        return self.departure_date + timedelta(days=self.duration_days)

    @property
    def reward(self) -> int:
        return self.base_reward * self.danger_multiplier

    @property
    def is_completed(self) -> bool:
        return self.returned_on is not None

    def is_overdue(self, today: date | None = None) -> bool:
        if today is None:
            today = date.today()

        return self.returned_on is None and self.due_date < today

    def mark_returned(self, on: date):
        if on <= self.departure_date:
            raise ValidationError("cannot return from mission before the departure")
        self.returned_on = on

    def days_late(self) -> int:
        reference_date = self.returned_on or date.today()

        return (reference_date - self.due_date).days

    def __eq__(self, other: Mission) -> bool:
        if not isinstance(other, Mission):
            return NotImplemented
        return (
            self.creature_name == other.creature_name
            and self.departure_date == other.departure_date
        )

    def __hash__(self) -> int:
        return hash((self.creature_name, self.departure_date))
