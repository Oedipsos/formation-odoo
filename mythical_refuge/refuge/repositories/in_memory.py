from refuge.exceptions import ValidationError, NotFoundError
from refuge.models.creature import Creature
from refuge.models.employee import Employee
from refuge.repositories.protocols import CreatureRepository, EmployeeRepository


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
            stored_creature.power_level = creature.power_level
            if hasattr(stored_creature, "resurrection_count"):
                stored_creature.resurrection_count = getattr(
                    creature, "resurrection_count", 0
                )
            stored_creature._in_refuge = creature.in_refuge
        except NotFoundError:
            return


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
