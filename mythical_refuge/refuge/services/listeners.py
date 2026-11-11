from refuge.notifiers.protocol import Notifier


class NotificationListener:
    def __init__(self, notifier: Notifier):
        self.notifier = notifier

    def on_started(self, mission: Mission) -> None:
        self.notifier.notify(
            "{} departed to {} with {} (due back {})".format(
                misison.creature_name,
                mission.destination,
                mission.handler_name,
                mission.due_date,
            )
        )

    def on_completed(self, mission: Mission) -> None:
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
