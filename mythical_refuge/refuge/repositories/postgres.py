import dataclasses

from refuge.db.connection import DatabaseConnection
from refuge.exceptions import ValidationError, NotFoundError
from refuge.models.creature import Creature
from refuge.models.employee import Employee
from refuge.models.health_record import HealthRecord, HealthStatus
from refuge.models.mission import Mission
from refuge.repositories.protocols import (
    CreatureRepository,
    EmployeeRepository,
    MissionRepository,
    HealthRecordRepository,
)
from refuge.repositories.factories import CreatureFactory, EmployeeFactory


class PostgresCreatureRepository:
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


class PostgresEmployeeRepository:
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


class PostgresMissionRepository:
    """
    Interface between the `missions` table and the client.
    """

    def __init__(self, db: DatabaseConnection):
        self.db = db

    def add(self, mission: Mission) -> Mission:
        """
        Insert a new mission into the database and sets its ID from the database's reply
        """
        c_name = mission.creature_name
        d_name = mission.destination
        h_name = mission.handler_name
        dep_date = mission.departure_date
        duration_days = mission.duration_days
        base_reward = mission.base_reward

        with self.db.cursor() as cur:
            cur.execute(
                """
                INSERT INTO missions (creature_id, handler_id, destination_id,
                    departure_date, duration_days, base_reward)
                SELECT c.id, e.id, d.id, %s, %s, %s
                FROM creatures c, employees e, destinations d
                WHERE c.name = %s AND d.name = %s AND e.full_name = %s
                RETURNING id
                """,
                (dep_date, duration_days, base_reward, c_name, d_name, h_name),
            )
            if cur.rowcount > 0:
                mission.id = cur.fetchone()["id"]
            else:
                raise NotFoundError("Unknown creature, handler or destination.")

            cur.execute(
                """
                SELECT danger_multiplier
                FROM missions m 
                JOIN destinations d ON d.id = m.destination_id
                WHERE d.name = %s
                """,
                (d_name,),
            )

            mission.danger_multiplier = cur.fetchone()["danger_multiplier"]

        return mission

    def list_all(self) -> list[Mission]:
        """
        Query all missions from the database ordered by departure date,
        and returns it as a list.
        """
        with self.db.cursor() as cur:
            cur.execute(
                """
                SELECT
                    m.id,
                    c.name as creature_name,
                    e.full_name as handler_name,
                    d.name as destination,
                    m.departure_date,
                    m.duration_days,
                    m.base_reward,
                    d.danger_multiplier,
                    m.returned_on, 
                    m.notes
                FROM missions m
                JOIN destinations d on d.id = m.destination_id
                JOIN creatures c on c.id = m.creature_id
                JOIN employees e on e.id = m.handler_id
                ORDER BY departure_date;
                """
            )
            rows = cur.fetchall()
        return [Mission(**row) for row in rows]

    def list_open_for_handler(self, handler_name: str) -> list[Mission]:
        """
        Query for all non-finished missions associate to handler whose name is `handler_name`,
        and returns a list of all such missions.
        """
        with self.db.cursor() as cur:
            cur.execute(
                """
                SELECT
                    m.id,
                    c.name as creature_name,
                    e.full_name as handler_name,
                    d.name as destination,
                    m.departure_date,
                    m.duration_days,
                    m.base_reward,
                    d.danger_multiplier,
                    m.returned_on, 
                    m.notes
                FROM missions m
                JOIN destinations d ON d.id = m.destination_id
                JOIN creatures c ON c.id = m.creature_id
                JOIN employees e ON e.id = m.handler_id
                    AND e.full_name = %s
                WHERE returned_on is NULL
                """,
                (handler_name,),
            )
            rows = cur.fetchall()
        return [Mission(**row) for row in rows]

    def get_open_for_creature(self, creature_name: str) -> Mission | None:
        """
        Retrieves the Mission where the creature named `creature_name` is sent, if any.
        Returns None if no such mission is found.
        """
        with self.db.cursor() as cur:
            cur.execute(
                """
                SELECT
                    m.id,
                    c.name as creature_name,
                    e.full_name as handler_name,
                    d.name as destination,
                    m.departure_date,
                    m.duration_days,
                    m.base_reward,
                    d.danger_multiplier,
                    m.returned_on, 
                    m.notes
                FROM missions m
                JOIN destinations d ON d.id = m.destination_id
                JOIN employees e ON e.id = m.handler_id
                JOIN creatures c ON c.id = m.creature_id
                    AND c.name = %s
                WHERE returned_on is NULL
                """,
                (creature_name,),
            )
            row = cur.fetchone()

        if row is not None:
            return Mission(**row)

        return None

    def update(self, mission: Mission) -> None:
        with self.db.cursor() as cur:
            cur.execute(
                """
                UPDATE missions
                    SET returned_on = %s
                WHERE id = %s
                """,
                (mission.returned_on, mission.id),
            )


class PostgresHealthRecordRepository:
    """
    Interface between the `heath_records` table and the client.
    """

    def __init__(self, db: DatabaseConnection):
        self.db = db

    def add(self, record: HealthRecord) -> HealthRecord:
        """
        Insert a new health_record into the database, and sets its ID from the database's reply.
        """
        creature_name = record.creature_name
        vet_name = record.vet_name
        examined_on = record.examined_on
        status = record.status
        diagnosis = record.diagnosis
        treatment = record.treatment

        with self.db.cursor() as cur:
            cur.execute(
                """
                INSERT INTO health_records (creature_id, vet_id, examined_on,
                        status, diagnosis, treatment)
                SELECT c.id, v.id, %s, %s, %s, %s
                FROM creatures c, employees v
                WHERE c.name = %s AND v.full_name = %s
                RETURNING id
                """,
                (examined_on, status, diagnosis, treatment, creature_name, vet_name),
            )
            id_ = cur.fetchone()["id"]

        return dataclasses.replace(record, id=id_)

    def latest_for(self, creature_name: str) -> HealthRecord | None:
        """
        Query all missions from the database ordered by departure date,
        and returns it as a list.
        """
        with self.db.cursor() as cur:
            cur.execute(
                """
                SELECT
                    r.id as id,
                    c.name as creature_name,
                    e.full_name as vet_name,
                    r.examined_on,
                    r.status,
                    r.diagnosis,
                    r.treatment
                FROM health_records r
                JOIN creatures c on c.id = r.creature_id
                    AND c.name = %s
                JOIN employees e on e.id = r.vet_id
                ORDER BY examined_on DESC, id DESC
                LIMIT 1
                """,
                (creature_name,),
            )
            row = cur.fetchone()

        if row is not None:
            row["status"] = HealthStatus(row["status"])
            return HealthRecord(**row)

        return None
