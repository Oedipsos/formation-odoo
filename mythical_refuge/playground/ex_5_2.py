from dataclasses import FrozenInstanceError
from datetime import date
from decimal import Decimal

from refuge.exceptions import ValidationError
from refuge.models.employee import Veterinarian
from refuge.models.health_record import HealthStatus
from refuge.models.mission import Mission
from refuge.models.species import Basilisk

m1 = Mission(
    "Frostbite",
    "Aldric Stone",
    "Frozen Peaks",
    date(2026, 1, 5),
    14,
    500,
    Decimal("2.0"),
)
m2 = Mission("Frostbite", "Brynn Ashford", "Northern Pass", date(2026, 1, 5), 3, 80)
m3 = Mission(
    "Ember", "Faye Lumen", "Frozen Peaks", date(2026, 3, 2), 7, 250, Decimal("2.0")
)

print(m1 == m2, hash(m1) == hash(m2), len({m1, m2, m3}))
print(m1.due_date, f"{m1.reward:.2f}")
print(m3.is_overdue(today=date(2026, 3, 15)), m3.is_overdue(today=date(2026, 3, 5)))

try:
    Mission("Ember", "Faye Lumen", "Frozen Peaks", date(2026, 3, 2), 0, 250)
except ValidationError as error:
    print(error)

m1.mark_returned(date(2026, 1, 20))
print(m1.is_completed, m1.days_late())

dara = Veterinarian("Dara Quill", "dara@refuge.example")
record = dara.perform_checkup(
    Basilisk("Gorgo", "Serpent Marsh", 91),
    HealthStatus.QUARANTINE,
    "Unstable petrifying gaze",
    "Isolation",
    on=date(2026, 2, 28),
)
print(record.status.value, record.status.allows_missions)
try:
    record.status = HealthStatus.HEALTHY
except FrozenInstanceError:
    print("health records are immutable")
