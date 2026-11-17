import abc
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date
from typing import Any, Protocol

Handler = Callable[[Any], None]


@dataclass(frozen=True)
class Event(abc.ABC):
    pass


@dataclass(frozen=True)
class MissionStarted(Event):
    mission: Mission


@dataclass(frozen=True)
class MissionCompleted(Event):
    mission: Mission


@dataclass(frozen=True)
class MissionRefused(Event):
    creature_name: str
    reason: str
    on: date


class EventBus:
    def __init__(self):
        self.subs: dict[Event, list[Handler]] = defaultdict(list)

    def subscribe(self, event_type: type[Event], handler: Handler) -> None:
        self.subs[event_type].append(handler)

    def publish(self, event: Event) -> None:
        event_type = type(event)

        if event_type not in self.subs:
            return

        for handler in self.subs[event_type]:
            handler(event)


class EventPublisher(Protocol):
    def publish(self, event) -> None:
        ...
