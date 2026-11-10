from datetime import date, timedelta
from decimal import Decimal

from refuge.algorithms.intervals import find_overlapping_pairs
from refuge.exceptions import MissionRefusedError, NotFoundError
from refuge.models.mission import Mission
from refuge.notifiers.protocol import Notifier
from refuge.repositories.protocols import (
    CreatureRepository,
    EmployeeRepository,
    MissionRepository,
    HealthRecordRepository,
    TransactionManager,
)


class MissionService:
    """docstring for MissionService"""

    def __init__(
        self,
        creatures: CreatureRepository,
        employees: EmployeeRepository,
        missions: MissionRepository,
        health: HealthRecordRepository,
        notifier: Notifier,
        tx: TransactionManager,
        clock: Callable[[], date] = date.today,
    ):
        super().__init__()
        self.creatures = creatures
        self.employees = employees
        self.missions = missions
        self.health = health
        self.notifier = notifier
        self._tx = tx
        self._clock = clock

    def dispatch(
        self,
        creature_name: str,
        handler_name: str,
        destination: str,
        base_reward: Decimal,
        departure_date: date | None = None,
    ):
        if departure_date is None:
            departure_date = self._clock()

        with self._tx.transaction():
            creature = self.creatures.get(creature_name)
            handler = self.employees.get(handler_name)
            handler_open_missions = self.missions.list_open_for_handler(handler_name)
            latest_report = self.health.latest_for(creature_name)

        if not creature.in_refuge:
            raise MissionRefusedError(f"{creature_name} is already on a mission")

        if latest_report is not None and not latest_report.status.allows_missions:
            status = latest_report.status
            raise MissionRefusedError(
                f"{creature_name} cannot leave: health status is {str(status)!r}"
            )

        if not handler.can_escort(creature):
            raise MissionRefusedError(
                f"{handler} is not allowed to escort {creature_name} (power {creature.power_level})"
            )

        due_date = departure_date + timedelta(days=creature.mission_duration_days())
        intervals = [(departure_date, due_date)]

        intervals.extend(
            [(m.departure_date, m.due_date) for m in handler_open_missions]
        )
        if p := find_overlapping_pairs(intervals):
            mission_idx = p[0][1] - 1
            current_mission = handler_open_missions[mission_idx]

            raise MissionRefusedError(
                f"{handler_name} is already escorting {current_mission.creature_name} until {current_mission.due_date}."
            )

        # Might raise MissionRefusedError depending on creature's mission requirements
        creature.send_on_mission()

        mission = Mission(
            creature_name,
            handler_name,
            destination,
            departure_date,
            creature.mission_duration_days(),
            base_reward,
        )
        with self._tx.transaction():
            mission = self.missions.add(mission)
            self.creatures.update(creature)

        self.notifier.notify(
            "{} departed to {} with {} (due back {}).".format(
                creature_name,
                mission.destination,
                handler_name,
                mission.due_date,
            )
        )

        return mission

    def recall(self, creature_name: str, returned_on: date | None = None) -> Mission:
        if returned_on is None:
            returned_on = self._clock()

        with self._tx.transaction():
            mission = self.missions.get_open_for_creature(creature_name)
            creature = self.creatures.get(creature_name)

        if mission is None:
            raise NotFoundError(f"{creature_name} has no open mission.")

        mission.mark_returned(returned_on)
        creature.return_to_refuge()

        with self._tx.transaction():
            self.missions.update(mission)
            self.creatures.update(creature)

        late = mission.days_late()
        late_msg = f" ({late} day{'s' if late > 1 else ''} late)"
        msg = "{} returned from {} - reward {:.2f} gold{}.".format(
            creature_name, mission.destination, mission.reward, late_msg if late else ""
        )

        self.notifier.notify(msg)
        return mission
