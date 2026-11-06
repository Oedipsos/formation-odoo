from datetime import date
from decimal import Decimal

from refuge.db.connection import DatabaseConnection
from refuge.exceptions import ValidationError
from refuge.models.mission import Mission
from refuge.repositories.in_memory import InMemoryMissionRepository
from refuge.repositories.postgres import (
    PostgresMissionRepository,
    PostgresHealthRecordRepository,
)


with DatabaseConnection() as db:
    missions = PostgresMissionRepository(db)
    health = PostgresHealthRecordRepository(db)

    for m in missions.list_open_for_handler("Faye Lumen"):
        print(
            m.creature_name, m.destination, m.due_date, m.is_overdue(date(2026, 3, 15))
        )
    print(missions.get_open_for_creature("Ignis"))
    all_missions = missions.list_all()
    print(
        len(all_missions),
        f"{sum(m.reward for m in all_missions if m.is_completed):.2f}",
    )
    print(
        health.latest_for("Stardust").status.value,
        health.latest_for("Gorgo").status.value,
    )
    print(health.latest_for("Sylph"))

    try:
        with db.transaction():
            missions.add(
                Mission(
                    "Ignis", "Aldric Stone", "Northern Pass", date(2026, 3, 15), 14, 300
                )
            )
            raise RuntimeError("Raven network down!")
    except RuntimeError as e:
        pass
    print(len(missions.list_all()))

memory = InMemoryMissionRepository(
    {"Northern Pass": Decimal("1.0"), "Frozen Peaks": Decimal("2.0")}
)
stored = memory.add(
    Mission("Talon", "Faye Lumen", "Frozen Peaks", date(2026, 2, 10), 10, Decimal(300))
)
print(stored.id, f"{stored.reward:.2f}")
try:
    memory.add(
        Mission(
            "Talon", "Aldric Stone", "Northern Pass", date(2026, 2, 10), 10, Decimal(50)
        )
    )
except ValidationError as error:
    print(error)
