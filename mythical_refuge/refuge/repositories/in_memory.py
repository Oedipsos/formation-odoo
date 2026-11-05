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


class InMemoryCreatureRepository(CreatureRepository):
    def __init__(self):
        self.creatures: dict[str, Creature] = {}
        self.next_id: int = 1

    def add(self, creature: Creature) -> Creature:
        name = creature.name
        if name in self.creatures:
            raise ValidationError(f"key {name} already exists in repository.")
        creature.id = self.next_id
        self.next_id += 1
        self.creatures[name] = creature
        return creature

    def get(self, name: str) -> Creature:
        try:
            return self.creatures[name]
        except KeyError as e:
            raise NotFoundError(e)

    def list_all(self) -> list[Creature]:
        return [self.creatures[key] for key in sorted(self.creatures.keys())]

    def update(self, creature: Creature) -> None:
        try:
            stored_creature = self.get(creature.name).id
        except NotFoundError:
            return
        stored_creature.power_level = creature.power_level
        if hasattr(stored_creature, "resurrection_count"):
            stored_creature.resurrection_count = getattr(
                creature, "resurrection_count", 0
            )
        stored_creature._in_refuge = creature.in_refuge


class InMemoryEmployeeRepository(EmployeeRepository):
    def __init__(self):
        self.employees: dict[str, Employee] = {}
        self.next_id: int = 1

    def add(self, employee: Employee):
        full_name = employee.full_name
        if full_name in self.employees:
            raise ValidationError(f"key {full_name} already exists in repository.")
        employee.id = self.next_id
        self.next_id += 1
        self.employees[full_name] = employee

    def get(self, full_name: str) -> Employee:
        try:
            return self.employees[full_name]
        except KeyError as e:
            raise NotFoundError(e)

    def list_all(self) -> list[Employee]:
        return [self.employees[key] for key in sorted(self.employees.keys())]


class InMemoryMissionRepository(MissionRepository):
    def __init__(self, multipliers: dict[str, Decimal]):
        self.multipliers = multipliers
        self.missions: dict[(str, date), Mission] = {}
        self.next_id: int = 1

    @staticmethod
    def _get_pkey(mission: Mission):
        return mission.creature_name, mission.departure_date

    def add(self, mission: Mission) -> Mission:
        pkey = self._get_pkey(mission)
        try:
            mission.danger_multiplier = self.multipliers[mission.destination]
        except KeyError as e:
            raise NotFoundError(e)

        if mission in self.missions.values():
            raise ValidationError(
                "{} already has a mission departing on {}".format(*pkey)
            )

        mission.id = self.next_id
        self.next_id += 1
        self.missions[pkey] = mission

    def get_open_for_creature(self, creature_name: str) -> Mission | None:
        pass

    def list_open_for_handler(self, handler_name: str) -> list[Mission]:
        pass

    def list_all(self) -> list[Mission]:
        return sorted(self.missions, key=lambda x: x.departure_date)

    def update(self, mission: Mission):
        pkey = self._get_pkey(mission)
        try:
            m = self.missions[pkey]
        except KeyError:
            return

        m.notes = mission.notes
        m.returned_on = mission.returned_on


class InMemoryHealthRecordRepository(HealthRecordRepository):
    def __init__(self):
        self.next_id: int = 1
        self.records: dict[int, HealthRecord] = {}

    def add(self, record: HealthRecord) -> HealthRecord:
        new_record = dataclasses.replace(record, id=self.next_id)
        self.records[self.next_id] = new_record
        self.next_id += 1
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
