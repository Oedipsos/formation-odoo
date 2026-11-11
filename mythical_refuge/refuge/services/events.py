from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class MissionStarted:
    mission: Mission


@dataclass(frozen=True)
class MissionCompleted:
    mission: Mission


@dataclass(frozen=True)
class MissionRefused:
    creature_name: str
    reason: str
    on: date


class EventBus:
    def __init__(self):
        ...

    def subscribe(self, event_type: type, handler: Callable[[Any], None]) -> None:
        ...

    def publish(self, event) -> None:
        ...
