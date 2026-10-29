from refuge.models.enclosure import Enclosure
from refuge.models.species import Dragon, Unicorn, Basilisk, Griffin
from refuge.exceptions import EnclosureFullError, IncompatibleSpeciesError

caves = Enclosure("Ember Caves", 3)
caves.add(Dragon("Frostbite", "Nordic Realms", 95, "ice"))
caves.add(Dragon("Ignis", "Volcanic Depths", 88, "fire"))

print(len(caves))
print("Frostbite" in caves, "Ember" in caves)
print(caves["Ignis"])
print(repr(caves))
for creature in caves:
    print(creature.name, "-", creature.travel_mode())

try:
    caves.add(Unicorn("Stardust", "Silver Woods", 45))
except IncompatibleSpeciesError as error:
    print("IncompatibleSpeciesError:", error)

caves.add(Basilisk("Gorgo", "Serpent Marsh", 91))
print(caves.is_full, caves.free_slots)

try:
    caves.add(Dragon("Cinder", "Ashlands", 60, "fire"))
except EnclosureFullError as error:
    print("EnclosureFullError:", error)

try:
    caves["Ember"]
except KeyError as error:
    print("KeyError:", error)

print(caves.remove("Ignis").name, repr(caves))
print(
    caves.can_accept(Unicorn("Pebble", "Misty Hills", 25)),
    caves.can_accept(Griffin("Talon", "Eagle Peaks", 80)),
)
