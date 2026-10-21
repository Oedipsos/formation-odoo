from refuge.exceptions import MissionRefusedError
from refuge.models.creature import Creature
from refuge.models.mixins import FlyingMixin


class Dragon(FlyingMixin, Creature):
    """docstring for Dragon"""

    def __init__(self, name, origin, power_level, element, **kwargs):
        super().__init__(name, "Dragon", origin, power_level, **kwargs)
        self.element = element

    def mission_duration_days(self) -> int:
        return 14

    def special_ability(self) -> str:
        name = self.name
        element = self.element
        return f"{name} breathes {element} and flies at great speed."

    def __str__(self) -> str:
        base = super().__str__()
        element = self.element
        return base + f" - element: {element}"

    def __repr__(self) -> str:
        name = self.name
        origin = self.origin
        power_level = self.power_level
        element = self.element
        return f"Dragon({name=}, {origin=}, {power_level=}, {element=})"


class Phoenix(FlyingMixin, Creature):
    """docstring for Phoenix"""

    def __init__(self, name, origin, power_level, resurrection_count=0, **kwargs):
        super().__init__(name, "Phoenix", origin, power_level, **kwargs)
        self.resurrection_count = resurrection_count

    def mission_duration_days(self) -> int:
        return 7

    def special_ability(self) -> str:
        name = self.name
        return f"{name} radiates a flame aura and rises again from its ashes."

    def resurrect(self) -> str:
        self.resurrection_count += 1
        resurrections = self.resurrection_count
        return f"Ember rises from its ashes! (resurrections: {resurrections})"


class Unicorn(Creature):
    """docstring for Unicorn"""

    MIN_MISSION_POWER = 40

    def __init__(self, name, origin, power_level, **kwargs):
        super().__init__(name, "Unicorn", origin, power_level, **kwargs)

    def mission_duration_days(self) -> int:
        return 3

    def special_ability(self) -> str:
        name = self.name
        return f"{name} heals its allies and gallops faster than the wind."

    def refusal_reason(self) -> None | str:
        name = self.name
        power = self.power_level
        if power < Unicorn.MIN_MISSION_POWER:
            return f"{name} is too weak for a mission (power {power} < {Unicorn.MIN_MISSION_POWER})."


class Griffin(FlyingMixin, Creature):
    """docstring for Griffin"""

    def __init__(self, name, origin, power_level, **kwargs):
        super().__init__(name, "Griffin", origin, power_level, **kwargs)

    def mission_duration_days(self) -> int:
        return 10

    def special_ability(self) -> str:
        name = self.name
        return f"{name} dives from the clouds with razor-sharp talons."


class Basilisk(Creature):
    """docstring for Basilisk"""

    def __init__(self, name, origin, power_level, **kwargs):
        super().__init__(name, "Basilisk", origin, power_level, **kwargs)

    def mission_duration_days(self) -> int:
        return 5

    def special_ability(self) -> str:
        name = self.name
        return f"{name} petrifies its enemies with a single gaze."


class WrongDragon(Creature, FlyingMixin):
    """docstring for Dragon"""

    def __init__(self, name, origin, power_level, element, **kwargs):
        super().__init__(name, "Dragon", origin, power_level, **kwargs)
        self.element = element

    def mission_duration_days(self) -> int:
        return 14

    def special_ability(self) -> str:
        name = self.name
        element = self.element
        return f"{name} breathes {element} and flies at great speed."

    def __str__(self) -> str:
        base = super().__str__()
        element = self.element
        return base + f" - element: {element}"

    def __repr__(self) -> str:
        name = self.name
        origin = self.origin
        power_level = self.power_level
        element = self.element
        return f"Dragon({name=}, {origin=}, {power_level=}, {element=})"


class StatueDragon(Dragon):
    """A stone dragon displayed at the refuge entrance."""

    def special_ability(self) -> str:
        raise NotImplementedError("Statues have no abilities.")

    def refusal_reason(self) -> str | None:
        return "A statue cannot move."


class RoboticGuard:
    def __init__(self, name: str, model: str):
        self.name = name
        self.model = model

    def special_ability(self) -> str:
        return f"{self.name} patrols the perimeter and fires laser beams."

    def mission_duration_days(self) -> int:
        return 1

    def __str__(self) -> str:
        return f"{self.name} [Robotic Guard — model {self.model}]"
