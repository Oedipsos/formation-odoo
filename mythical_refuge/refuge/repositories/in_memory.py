import contextlib
import dataclasses
from datetime import date
from decimal import Decimal

from refuge.exceptions import ValidationError, NotFoundError
from refuge.models.creature import Creature
from refuge.models.employee import Employee
from refuge.models.health_record import HealthRecord
from refuge.models.mission import Mission
from refuge.repositories.protocols import (
    CreatureRepository,
    EmployeeRepository,
    HealthRecordRepository,
    MissionRepository,
)


class InMemoryCreatureRepository:
    """
    Memory representation of a database, mocking the 'creature' table interface.
    """

    def __init__(self):
        self.creatures: dict[str, Creature] = {}
        self.__next_id: int = 0

    def _next_id(self):
        id = self.__next_id
        self.__next_id += 1
        return id

    def add(self, creature: Creature) -> Creature:
        name = creature.name

        if name in self.creatures:
            raise ValidationError(f"key {name} already exists in repository.")

        creature.id = self._next_id()
        self.creatures[name] = creature
        return creature

    def get(self, name: str) -> Creature:
        """Returns creature associated to `name` if registered, else raises NotFoundError"""
        try:
            return self.creatures[name]
        except KeyError as e:
            raise NotFoundError(e)

    def list_all(self) -> list[Creature]:
        return [self.creatures[key] for key in sorted(self.creatures.keys())]

    def update(self, creature: Creature) -> None:
        try:
            stored_creature = self.get(creature.name)
        except NotFoundError:
            return
        stored_creature.power_level = creature.power_level

        # Try to set resurrection_count only if creature has that attribute
        if hasattr(stored_creature, "resurrection_count"):
            stored_creature.resurrection_count = getattr(
                creature, "resurrection_count", 0
            )
        stored_creature._in_refuge = creature.in_refuge


class InMemoryEmployeeRepository:
    """
    Memory representation of a database, mocking the 'employee' table interface.
    """

    def __init__(self):
        self.employees: dict[str, Employee] = {}
        self.__next_id: int = 0

    def _next_id(self):
        id = self.__next_id
        self.__next_id += 1
        return id

    def add(self, employee: Employee) -> Employee:
        full_name = employee.full_name
        if full_name in self.employees:
            raise ValidationError(f"key {full_name} already exists in repository.")
        employee.id = self._next_id()
        self.employees[full_name] = employee
        return employee

    def get(self, full_name: str) -> Employee:
        try:
            return self.employees[full_name]
        except KeyError as e:
            raise NotFoundError(e)

    def list_all(self) -> list[Employee]:
        return [self.employees[key] for key in sorted(self.employees.keys())]


class InMemoryMissionRepository:
    """
    Memory representation of a database, mocking the 'missions' table interface.
    """

    def __init__(self, multipliers: dict[str, Decimal]):
        self.multipliers = multipliers
        self.missions: dict[tuple[str, date], Mission] = {}
        self.__next_id: int = 0

    @staticmethod
    def _get_pkey(mission: Mission) -> tuple[str, date]:
        return mission.creature_name, mission.departure_date

    def _next_id(self):
        id = self.__next_id
        self.__next_id += 1
        return id

    def add(self, mission: Mission) -> Mission:
        pkey = self._get_pkey(mission)
        dest = mission.destination

        if dest not in self.multipliers:
            raise NotFoundError(repr(d))

        if mission in self.missions.values():
            raise ValidationError(
                "{} already has a mission departing on {}".format(*pkey)
            )

        mission.id = self._next_id()
        mission.danger_multiplier = self.multipliers[dest]
        self.missions[pkey] = mission
        return mission

    def get_open_for_creature(self, creature_name: str) -> Mission | None:
        return next(
            (
                m
                for m in self.missions.values()
                if m.creature_name == creature_name and m.returned_on is None
            ),
            None,
        )

    def list_open_for_handler(self, handler_name: str) -> list[Mission]:
        return list(
            m
            for m in self.missions.values()
            if m.handler_name == handler_name and m.returned_on is None
        )

    def list_all(self) -> list[Mission]:
        return sorted(self.missions.values(), key=lambda x: x.departure_date)

    def update(self, mission: Mission):
        pkey = self._get_pkey(mission)
        try:
            m = self.missions[pkey]
        except KeyError:
            return

        m.notes = mission.notes
        m.returned_on = mission.returned_on


class InMemoryHealthRecordRepository:
    """
    Memory representation of a database, mocking the 'health_records' table interface.
    """

    def __init__(self):
        self.records: dict[int, HealthRecord] = {}
        self.__next_id: int = 0

    def _next_id(self):
        id = self.__next_id
        self.__next_id += 1
        return id

    def add(self, record: HealthRecord) -> HealthRecord:
        id = self._next_id()
        new_record = dataclasses.replace(record, id=id)
        self.records[id] = new_record
        return new_record

    def latest_for(self, creature_name: str) -> HealthRecord | None:
        sorted_records = sorted(self.records.values(), key=lambda x: x.examined_on)
        return next(
            (
                record
                for record in sorted_records
                if record.creature_name == creature_name
            ),
            None,
        )


class NoTransaction:
    """Dummy context manager exposing the `TransactionProtocol`. For use with in-memory repositories only"""

    def transaction(self):
        return contextlib.nullcontext()
