import abc

from refuge.exceptions import ValidationError, MissionRefusedError


class Creature(abc.ABC):
    _total_creatures = 0
    VALID_SPECIES = frozenset(("Dragon", "Phoenix", "Unicorn", "Griffin", "Basilisk"))

    def __init__(self, name: str, species: str, origin: str, power_level: int):
        super().__init__()

        if Creature.is_valid_species(species):
            self.species = species
        else:
            raise ValidationError(f"{species!r} is not a valid species.")

        self.name = name
        self.__origin = origin
        self.power_level = power_level
        self._in_refuge = True

        Creature._total_creatures += 1

    def __str__(self) -> str:
        location = "in refuge" if self._in_refuge else "on mission"
        name = self.name
        species = self.species
        origin = self.origin
        ret = f"{name} the {species} (origin: {origin}) [{location}]"
        return ret

    def __repr__(self) -> str:
        name = self.name
        species = self.species
        origin = self.origin
        power_level = self.power_level

        return f"Creature({name=}, {species=}, {origin=}, {power_level=})"

    @classmethod
    def from_dict(cls, dict_: dict[str, str | int]) -> Creature:
        name = dict_["name"]
        species = dict_["species"]
        origin = dict_["origin"]
        power_level = dict_["power_level"]

        return cls(name, species, origin, power_level)

    @classmethod
    def from_string(cls, text: str) -> Creature:
        name, species, origin, power_level = [s.strip() for s in text.split(",")]
        power_level = int(power_level)

        return cls(name, species, origin, power_level)

    def travel_mode(self) -> str:
        return "on foot"

    @property
    def in_refuge(self):
        return self._in_refuge

    @property
    def origin(self) -> str:
        return self.__origin

    @property
    def power_level(self) -> int:
        return self._power_level

    @power_level.setter
    def power_level(self, value: int):
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValidationError(
                f"power_level must be an int, got {type(value).__name__}."
            )

        if not 0 <= value <= 100:
            raise ValidationError(
                f"power_level must be between 0 and 100, got {value}."
            )

        self._power_level = value

    def send_on_mission(self):
        """
        Raises MissionRefusedError when the creature cannot leave.
        """
        if not self._in_refuge:
            raise MissionRefusedError(f"{self.name} is already on a mission.")

        if (message := self.refusal_reason()) is not None:
            raise MissionRefusedError(message)

        self._in_refuge = False

    def return_to_refuge(self):
        self._in_refuge = True

    def refusal_reason(self) -> None | str:
        pass

    @staticmethod
    def is_valid_species(species: str) -> bool:
        return species in Creature.VALID_SPECIES

    @classmethod
    def get_total_creatures(cls) -> int:
        return cls._total_creatures

    @abc.abstractmethod
    def mission_duration_days() -> int:
        pass

    @abc.abstractmethod
    def special_ability() -> str:
        pass
