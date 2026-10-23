from abc import ABC, abstractmethod

from refuge.exceptions import ValidationError
from refuge.models.creature import Creature


class Employee(ABC):
    ROLE: str = "employee"
    PERMISSIONS: frozenset[str] = frozenset()

    def __init__(self, full_name: str, email: str):
        super().__init__()

    def can(self, permission: str) -> bool:
        pass

    def can_escort(self, creature: Creature) -> bool:
        pass

    @abstractmethod
    def decribe_duties(self) -> str:
        pass

    def __str__(self) -> str:
        return f"{full_name} ({self.ROLE})"


class Handler(Employee):
    ROLE = "handler"
    PERMISSIONS = frozenset({"escort_mission"})

    @property
    def certification_level(self):
        return self._certification_level

    @certification_level.setter
    def certification_level(self, value):
        if not (0 < value <= 5):
            raise ValidationError(
                "certification_level must be between 1 and 5, got", value
            )

        self._certification_level = value

    def can_escort(self, creature: Creature) -> bool:
        return self.certification_level * 20 >= creature.power_level

    def decribe_duties(self) -> str:
        escort_power = self.certification_level * 20
        return f"{full_name} escorts creatures up to power {escort_power}."

    def __str__(self) -> str:
        name = self.full_name
        role = self.ROLE
        level = self.certification_level
        return f"{name} ({role}, level {level})"


class Veterinarian(Employee):
    ROLE = "veterinarian"
    PERMISSIONS = frozenset({"perform_checkup"})

    def describe_duties(self) -> str:
        name = self.full_name
        return f"{name} examines and treats the creatures"

    def perform_checkup(self, creature: Creature, diagnosis: str) -> str:
        name = self.full_name
        c_name = creature.name
        return f"{name} examined {c_name}: {diagnosis}"
