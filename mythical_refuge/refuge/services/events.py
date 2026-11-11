from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from typing import Protocol


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
        self.subs = defaultdict(list)

    def subscribe(self, event_type: type, handler: Callable[[Any], None]) -> None:
        self.subs[event_type].append(handler)

    def publish(self, event) -> None:
        event_type = type(event)

        if event_type not in self.subs:
            return

        for handler in self.subs[event_type]:
            handler()


class EventPublisher(Protocol):
    def publish(self, event) -> None:
        ...
