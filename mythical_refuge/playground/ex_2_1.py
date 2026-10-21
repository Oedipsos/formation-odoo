from refuge.exceptions import MissionRefusedError
from refuge.models.creature import Creature
from refuge.models.species import Dragon, Phoenix, Unicorn, Griffin


def send_to_field(creature: Creature) -> None:
    try:
        creature.send_on_mission()
    except MissionRefusedError as e:
        print("Refused:", e)

    print(creature.special_ability())

    duration = creature.mission_duration_days()

    print(f"  Away for {duration} days")


residents = [
    Dragon("Frostbite", "Nordic Realms", 95, "ice"),
    Phoenix("Ember", "Ashlands", 72),
    Unicorn("Pebble", "Misty Hills", 25),
    Griffin("Talon", "Eagle Peaks", 80),
]
for resident in residents:
    send_to_field(resident)

print(residents[0])
print(repr(residents[0]))
print(residents[1].resurrect())

try:
    Creature("Nobody", "Dragon", "Nowhere", 10)
except TypeError:
    print("Creature is abstract")
