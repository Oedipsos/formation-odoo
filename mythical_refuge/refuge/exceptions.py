class RefugeError(Exception):
    pass


class ValidationError(RefugeError):
    pass


class MissionRefusedError(RefugeError):
    pass


class EnclosureFullError(RefugeError):
    pass


class IncompatibleSpeciesError(RefugeError):
    pass
