from refuge.exceptions import ValidationError
from refuge.models.creature import Creature

frostbite = Creature("Frostbite", "Dragon", "Nordic Realms", 95)
print(repr(frostbite))

frostbite.power_level = 80
print(frostbite.power_level)

for bad_value in (150, -3, "95", True):
    try:
        frostbite.power_level = bad_value
    except ValidationError as error:
        print(error)

try:
    frostbite.origin = "Elsewhere"
except AttributeError:
    print("origin is read-only")

print(frostbite._Creature__origin)
print(frostbite.in_refuge)
