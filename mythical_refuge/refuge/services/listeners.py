from refuge.notifiers.protocol import Notifier
from refuge.services.events import Event


class NotificationListener:
    def __init__(self, notifier: Notifier):
        self.notifier = notifier

    def on_started(self, event: Event) -> None:
        mission = event.mission
        self.notifier.notify(
            "{} departed to {} with {} (due back {})".format(
                mission.creature_name,
                mission.destination,
                mission.handler_name,
                mission.due_date,
            )
        )

    def on_completed(self, event: Event) -> None:
        mission = event.mission
        late = mission.days_late()
        late_str = f" ({late} day{'s' if late > 1 else ''} late)"
        self.notifier.notify(
            "{} returned from {} - reward {:.2f}{}.".format(
                mission.creature_name,
                mission.destination,
                mission.reward,
                late_str,
            )
        )


class AuditTrail:
    def __init__(self, path: str):
        self.path = path

    def on_started(self, event: Event):
        mission = event.mission
        with open(self.path, "a") as log:
            log.write(
                "{};{};{};{}".format(
                    mission.departure_date,
                    event,
                    mission.creature_name,
                    mission.destination,
                )
            )
            log.write("\n")

    def on_completed(self, event: Event):
        mission = event.mission
        with open(self.path, "a") as log:
            log.write(
                "{};{};{};{}".format(
                    mission.returned_on,
                    event,
                    mission.creature_name,
                    mission.destination,
                )
            )
            log.write("\n")

    def on_refused(self, event: Event):
        with open(self.path, "a") as log:
            log.write(
                "{};{};{};{}".format(
                    event.on,
                    event,
                    event.creature_name,
                    event.reason,
                )
            )
            log.write("\n")
