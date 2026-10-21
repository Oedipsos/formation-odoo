class RefugeError(Exception):
    pass


class ValidationError(RefugeError):
    pass


class MissionRefusedError(RefugeError):
    pass
