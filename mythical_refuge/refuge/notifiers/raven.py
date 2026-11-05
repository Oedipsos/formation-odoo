from refuge.exceptions import NotificationError


class RavenPost:
    """Third-party raven-post client (vendored). Do NOT modify."""

    def dispatch_raven(self, recipient: str, scroll: str) -> bool:
        print(f'^v^ Raven flies to {recipient}: "{scroll}"')
        return True


class RavenNotifier:
    def __init__(self, raven: RavenPost, recipient: str):
        self.raven = raven
        self.recipient = recipient

    def notify(self, message: str):
        if not self.raven.dispatch_raven(self.recipient, message):
            raise NotificationError(
                "Issue during message delivery (maybe a lost arrow)"
            )
