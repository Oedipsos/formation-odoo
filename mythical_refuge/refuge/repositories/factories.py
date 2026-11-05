from refuge.models.species import (
    Dragon,
    Phoenix,
    Unicorn,
    Griffin,
    Basilisk,
)
from refuge.models.creature import Creature
from refuge.models.employee import Employee, Veterinarian, Handler


class CreatureFactory:
    _REGISTRY: dict[str, type[Creature]] = {
        "Dragon": Dragon,
        "Phoenix": Phoenix,
        "Unicorn": Unicorn,
        "Basilisk": Basilisk,
        "Griffin": Griffin,
    }

    @classmethod
    def create(cls, data: dict[str, str | int]) -> Creature:
        species = data.pop("species")

        try:
            class_ = cls._REGISTRY[species]
        except KeyError:
            raise ValueError(f"Unknown species {species!r}")

        return class_.from_dict(data)


class EmployeeFactory:
    _REGISTRY: dict[str, type[Employee]] = {
        "handler": Handler,
        "veterinarian": Veterinarian,
    }

    @classmethod
    def create(cls, data: dict[str, str | int]) -> Employee:
        role = data.pop("role")

        try:
            class_ = _REGISTRY[role]
        except KeyError:
            raise ValueError(f"Unknown role {role!r}")

        return class_.from_dict()
