from contextlib import AbstractContextManager
from typing import Protocol

from refuge.models.creature import Creature
from refuge.models.employee import Employee
from refuge.models.health_record import HealthRecord
from refuge.models.mission import Mission


class CreatureRepository(Protocol):
    def add(self, creature: Creature) -> Creature:
        ...  # sets creature.id and returns it

    def get(self, name: str) -> Creature:
        ...  # raises NotFoundError

    def list_all(self) -> list[Creature]:
        ...  # ordered by name

    def update(self, creature: Creature) -> None:
        ...  # persists power_level, in_refuge, resurrection_count


class EmployeeRepository(Protocol):
    def add(self, employee: Employee) -> Employee:
        ...

    def get(self, full_name: str) -> Employee:
        ...  # raises NotFoundError

    def list_all(self) -> list[Employee]:
        ...


class MissionRepository(Protocol):
    def add(self, mission: Mission) -> Mission:
        ...  # sets id and danger_multiplier

    def get_open_for_creature(self, creature_name: str) -> Mission | None:
        ...

    def list_open_for_handler(self, handler_name: str) -> list[Mission]:
        ...

    def list_all(self) -> list[Mission]:
        ...  # ordered by departure date

    def update(self, mission: Mission) -> None:
        ...  # persists returned_on and notes


class HealthRecordRepository(Protocol):
    def add(self, record: HealthRecord) -> HealthRecord:
        ...  # returns a copy with its id

    def latest_for(self, creature_name: str) -> HealthRecord | None:
        ...


class TransactionManager(Protocol):
    def transaction(self) -> AbstractContextManager[None]:
        ...
