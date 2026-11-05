from typing import Protocol

from refuge.models.creature import Creature
from refuge.models.employee import Employee


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
