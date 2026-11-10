from datetime import date
from decimal import Decimal

from refuge.db.connection import DatabaseConnection
from refuge.exceptions import RefugeError
from refuge.models.health_record import HealthStatus
from refuge.models.species import Dragon, Basilisk, Unicorn
from refuge.models.employee import Handler, Veterinarian
from refuge.notifiers.console import ConsoleNotifier
from refuge.services.mission_service import MissionService
from refuge.repositories.in_memory import (
    InMemoryMissionRepository,
    InMemoryCreatureRepository,
    InMemoryEmployeeRepository,
    InMemoryHealthRecordRepository,
    NoTransaction,
)
from refuge.repositories.postgres import (
    PostgresMissionRepository,
    PostgresCreatureRepository,
    PostgresEmployeeRepository,
    PostgresHealthRecordRepository,
)


# Test in memory
creatures = InMemoryCreatureRepository()
for creature in [
    Dragon("Frostbite", "Nordic Realms", 95, "ice"),
    Unicorn("Moonbeam", "Crystal Lake", 67),
    Unicorn("Pebble", "Misty Hills", 25),
    Unicorn("Willow", "Moon Meadows", 42),
    Basilisk("Gorgo", "Serpent Marsh", 91),
]:
    creatures.add(creature)

employees = InMemoryEmployeeRepository()
employees.add(Handler("Aldric Stone", "aldric@refuge.example", 5))
employees.add(Handler("Brynn Ashford", "brynn@refuge.example", 3))
dara = employees.add(Veterinarian("Dara Quill", "dara@refuge.example"))

health = InMemoryHealthRecordRepository()
health.add(
    dara.perform_checkup(
        creatures.get("Gorgo"),
        HealthStatus.QUARANTINE,
        "Unstable petrifying gaze",
        on=date(2026, 2, 28),
    )
)

missions = InMemoryMissionRepository(
    {"Northern Pass": Decimal("1.0"), "Shadow Forest": Decimal("3.0")}
)
service = MissionService(
    creatures,
    employees,
    missions,
    health,
    ConsoleNotifier(),
    NoTransaction(),
    clock=lambda: date(2026, 3, 15),
)

attempts = [
    ("Frostbite", "Aldric Stone", "Shadow Forest", 700),
    ("Gorgo", "Aldric Stone", "Northern Pass", 300),
    ("Willow", "Aldric Stone", "Northern Pass", 60),
    ("Moonbeam", "Brynn Ashford", "Northern Pass", 120),
    ("Pebble", "Brynn Ashford", "Northern Pass", 40),
    ("Frostbite", "Aldric Stone", "Northern Pass", 100),
    ("Willow", "Dara Quill", "Northern Pass", 60),
]

for attempt in attempts:
    try:
        service.dispatch(*attempt)
    except RefugeError as error:
        print(f"{type(error).__name__}: {error}")

service.recall("Frostbite", returned_on=date(2026, 3, 30))
service.dispatch(
    "Willow", "Aldric Stone", "Northern Pass", 60, departure_date=date(2026, 3, 30)
)
try:
    service.recall("Moonbeam")
except RefugeError as error:
    print(f"{type(error).__name__}: {error}")
print(creatures.get("Frostbite"))
print(creatures.get("Willow"))
print()

# Test with PostGreSQL Database
with DatabaseConnection() as db:
    service = MissionService(
        PostgresCreatureRepository(db),
        PostgresEmployeeRepository(db),
        PostgresMissionRepository(db),
        PostgresHealthRecordRepository(db),
        ConsoleNotifier(),
        db,
        clock=lambda: date(2026, 3, 15),
    )
    actions = [
        lambda: service.dispatch("Gorgo", "Aldric Stone", "Northern Pass", 300),
        lambda: service.dispatch("Moonbeam", "Faye Lumen", "Northern Pass", 120),
        lambda: service.recall("Frostbite"),
        lambda: service.dispatch("Ignis", "Aldric Stone", "Northern Pass", 300),
        lambda: service.dispatch("Sylph", "Brynn Ashford", "Frozen Peaks", 150),
        lambda: service.dispatch("Talon", "Aldric Stone", "Frozen Peaks", 300),
    ]
    for action in actions:
        try:
            action()
        except RefugeError as error:
            print(f"{type(error).__name__}: {error}")
