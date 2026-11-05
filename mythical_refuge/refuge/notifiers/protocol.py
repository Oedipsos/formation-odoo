from typing import Protocol


class Notifier(Protocol):
    def notify(self, massage: str) -> None:
        ...
