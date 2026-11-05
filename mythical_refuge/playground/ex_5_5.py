from refuge.notifiers.console import ConsoleNotifier
from refuge.notifiers.file import FileNotifier
from refuge.notifiers.raven import RavenPost, RavenNotifier
from refuge.notifiers.silent import SilentNotifier
from refuge.notifiers.protocol import Notifier


class BrokenNotifier:
    """
    This class will trigger an error in mypy on purpose, to test the Notifier
    protocol, by defining `send` instead of `notify`.
    """

    def send(self, message: str):
        print(message)


def broadcast(notifier: Notifier, messages: list[str]):
    for message in messages:
        notifier.notify(message)


messages = ["Frostbite leaves for Shadow Forest.", "Ember is back."]
broadcast(ConsoleNotifier(), messages)
broadcast(SilentNotifier(), messages)

try:
    broadcast(BrokenNotifier(), messages)
except AttributeError:
    print('"notify" is not implemented')

broadcast(FileNotifier("mirror_log.txt"), messages)
broadcast(RavenNotifier(RavenPost(), "Head Keeper"), messages[:1])
