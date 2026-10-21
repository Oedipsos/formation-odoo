class FlyingMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flight_log: list[str] = []

    def travel_mode(self) -> str:
        return "by air"

    def fly(self, destination: str) -> str:
        name = self.name
        log = f"{name} soars toward {destination}."
        self.flight_log.append(log)
        return log
