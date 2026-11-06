from dataclasses import dataclass, field
from datetime import date
from enum import StrEnum


from refuge.exceptions import ValidationError


class HealthStatus(StrEnum):
    HEALTHY = "healthy"
    UNDER_OBSERVATION = "under observation"
    IN_TREATMENT = "in treatment"
    QUARANTINE = "quarantine"

    @property
    def allows_missions(self):
        return self in (HealthStatus.HEALTHY, HealthStatus.UNDER_OBSERVATION)


@dataclass(frozen=True)
class HealthRecord:
    creature_name: str
    vet_name: str
    examined_on: date
    status: HealthStatus
    diagnosis: str
    treatment: str = ""
    id: int | None = field(default=None, compare=False)

    def __post_init__(self):
        if not self.diagnosis:
            raise ValidationError("empty diagnosis.")
