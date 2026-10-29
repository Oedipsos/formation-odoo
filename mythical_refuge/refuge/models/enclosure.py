from refuge.exceptions import (
    ValidationError,
    IncompatibleSpeciesError,
    EnclosureFullError,
)
from refuge.models.creature import Creature


class Enclosure:
    INCOMPATIBLE_PAIRS = frozenset(
        {
            frozenset({"Dragon", "Unicorn"}),
            frozenset({"Basilisk", "Phoenix"}),
            frozenset({"Basilisk", "Unicorn"}),
        }
    )

    def __init__(self, name: str, capacity: int):
        if capacity <= 0:
            raise ValidationError("capacity must be strictly positive.")
        self._creatures: list[Creature] = []
        self.capacity = capacity
        self.name = name

        super().__init__()

    def __iter__(self):
        yield from self._creatures

    def __contains__(self, item) -> bool:
        return item in self._creature_names

    def __len__(self) -> int:
        return len(self._creatures)

    def __getitem__(self, item: str) -> Creature:
        for creature in self:
            if item == creature.name:
                return creature

        raise KeyError(item)

    def __repr__(self) -> str:
        names = [c.name for c in self]
        return (
            f"Enclosure({self.name!r}, {len(self)}/{self.capacity}: "
            f"{self._creature_names})"
        )

    @property
    def _creature_names(self):
        return [c.name for c in self]

    @property
    def free_slots(self) -> int:
        return self.capacity - len(self)

    @property
    def is_full(self) -> bool:
        return len(self) == self.capacity

    @property
    def species(self) -> set[str]:
        return {c.species for c in self}

    def _check_pair_compatibility(self, creature) -> tuple[str, bool]:
        new_set = self.species | {creature.species}

        for pair in self.INCOMPATIBLE_PAIRS:
            if pair <= new_set:
                (other,) = pair - {creature.species}
                return other, False
        return "", True

    def can_accept(self, creature: Creature) -> bool:
        _, compatible = self._check_pair_compatibility(creature)
        return compatible

    def add(self, creature: Creature):
        if creature.name in self:
            raise ValidationError(f"{creature.name!r} is already in {self.name}.")

        if self.is_full:
            raise EnclosureFullError(
                f"{self.name} is full (max capacity is {self.capacity})."
            )

        other, compatible = self._check_pair_compatibility(creature)
        if not compatible:
            raise IncompatibleSpeciesError(
                f"A {creature.species} cannot live with a {other} in {self.name}."
            )

        self._creatures.append(creature)

    def remove(self, name: str) -> Creature:
        for i, creature in enumerate(self):
            if creature.name == name:
                return self._creatures.pop(i)
