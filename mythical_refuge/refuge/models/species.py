from refuge.exceptions import MissionRefusedError
from refuge.models.creature import Creature
from refuge.models.mixins import FlyingMixin


class Dragon(FlyingMixin, Creature):
    def __init__(self, name, origin, power_level, element, **kwargs):
        super().__init__(name, "Dragon", origin, power_level, **kwargs)
        self.element = element

    @classmethod
    def from_dict(cls, dict_: dict):
        name = dict_.pop("name")
        origin = dict_.pop("origin")
        power_level = dict_.pop("power_level")
        element = dict_.pop("element")

        return cls(name, origin, power_level, element, **dict_)

    def to_dict(self) -> dict:
        dict_ = super().to_dict()
        dict_["element"] = self.element
        return dict_

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
    def __init__(self, name, origin, power_level, resurrection_count=0, **kwargs):
        self.resurrection_count = (
            kwargs.pop("resurrection_count", None) or resurrection_count
        )
        super().__init__(name, "Phoenix", origin, power_level, **kwargs)

    @classmethod
    def from_dict(cls, dict_: dict):
        name = dict_.pop("name")
        origin = dict_.pop("origin")
        power_level = dict_.pop("power_level")

        return cls(name, origin, power_level, **dict_)

    def to_dict(self) -> dict:
        dict_ = super().to_dict()
        dict_["resurrection_count"] = self.resurrection_count
        return dict_

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
    MIN_MISSION_POWER = 40

    def __init__(self, name, origin, power_level, **kwargs):
        super().__init__(name, "Unicorn", origin, power_level, **kwargs)

    @classmethod
    def from_dict(cls, dict_: dict):
        name = dict_.pop("name")
        origin = dict_.pop("origin")
        power_level = dict_.pop("power_level")

        return cls(name, origin, power_level, **dict_)

    def mission_duration_days(self) -> int:
        return 3

    def special_ability(self) -> str:
        name = self.name
        return f"{name} heals its allies and gallops faster than the wind."

    def refusal_reason(self) -> str | None:
        name = self.name
        power = self.power_level
        if power < Unicorn.MIN_MISSION_POWER:
            return f"{name} is too weak for a mission (power {power} < {Unicorn.MIN_MISSION_POWER})."


class Griffin(FlyingMixin, Creature):
    def __init__(self, name, origin, power_level, **kwargs):
        super().__init__(name, "Griffin", origin, power_level, **kwargs)

    @classmethod
    def from_dict(cls, dict_: dict):
        name = dict_.pop("name")
        origin = dict_.pop("origin")
        power_level = dict_.pop("power_level")

        return cls(name, origin, power_level, **dict_)

    def mission_duration_days(self) -> int:
        return 10

    def special_ability(self) -> str:
        name = self.name
        return f"{name} dives from the clouds with razor-sharp talons."


class Basilisk(Creature):
    def __init__(self, name, origin, power_level, **kwargs):
        super().__init__(name, "Basilisk", origin, power_level, **kwargs)

    @classmethod
    def from_dict(cls, dict_: dict):
        name = dict_.pop("name")
        origin = dict_.pop("origin")
        power_level = dict_.pop("power_level")

        return cls(name, origin, power_level, **dict_)

    def mission_duration_days(self) -> int:
        return 5

    def special_ability(self) -> str:
        name = self.name
        return f"{name} petrifies its enemies with a single gaze."
