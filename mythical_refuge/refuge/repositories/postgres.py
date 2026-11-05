from refuge.db.connection import DatabaseConnection
from refuge.exceptions import ValidationError, NotFoundError
from refuge.models.creature import Creature
from refuge.models.employee import Employee
from refuge.repositories.protocols import CreatureRepository, EmployeeRepository
from refuge.repositories.factories import CreatureFactory, EmployeeFactory


class PostgresCreatureRepository(CreatureRepository):
    def __init__(self, db: DatabaseConnection):
        # We're assuming db connection is open, since DatabaseConnection
        # should raise if it is closed anyways
        self.db = db

    def add(self, creature: Creature) -> Creature:
        name = creature.name
        species = creature.species
        origin = creature.origin
        power = creature.power_level
        res_count = getattr(creature, "resurrection_count", 0)
        element = getattr(creature, "element", None)
        in_refuge = creature.in_refuge

        with self.db.cursor() as cur:
            cur.execute(
                """
                INSERT INTO creatures (name, species, origin, power_level,
                        resurrection_count, element, in_refuge)
                VALUES %s
                RETURNING id
                """,
                ((name, species, origin, power, res_count, element, in_refuge),),
            )
            creature.id = cur.fetchone()["id"]

        return creature

    def get(self, name: str) -> Creature:
        with self.db.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM creatures
                WHERE name = %s
                """,
                (name,),
            )
            row = cur.fetchone()
        if row is None:
            raise NotFoundError(f"No creature named {name!r}.")
        return CreatureFactory.create(row)

    def list_all(self) -> list[Creature]:
        with self.db.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM creatures
                ORDER BY name
                """
            )
            rows = cur.fetchall()

        return [CreatureFactory.create(row) for row in rows]

    def update(self, creature: Creature):
        name = creature.name
        power = creature.power_level
        in_refuge = creature.in_refuge
        res_count = getattr(creature, "resurrection_count", 0)

        with self.db.cursor() as cur:
            cur.execute(
                """
                UPDATE creatures
                    SET power_level = %s,
                        in_refuge = %s,
                        resurrection_count = %s
                WHERE name = %s
                """,
                (power, in_refuge, res_count, name),
            )


class PostgresEmployeeRepository(EmployeeRepository):
    def __init__(self, db: DatabaseConnection):
        # We're assuming db connection is open, since DatabaseConnection
        # should raise if it is closed anyways
        self.db = db

    def add(self, employee: Employee) -> Employee:
        name = employee.full_name
        email = employee.email
        role = employee.ROLE
        cert_level = getattr(employee, "certification_level", None)

        with self.db.cursor() as cur:
            cur.execute(
                """
                INSERT INTO employees (full_name, email, role, certification_level)
                VALUES %s
                RETURNING id
                """,
                ((name, email, role, cert_level),),
            )
            employee.id = cur.fetchone()["id"]

        return employee

    def get(self, full_name: str) -> Employee:
        with self.db.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM employees
                WHERE full_name = %s
                """,
                (full_name,),
            )
            row = cur.fetchone()

        if row is None:
            raise NotFoundError(f"No employee named {full_name!r}.")

        return EmployeeFactory.create(row)

    def list_all(self) -> list[Employee]:
        with self.db.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM employees
                ORDER BY full_name
                """
            )
            rows = cur.fetchall()

        return [EmployeeFactory.create(row) for row in rows]
