from refuge.models.creature import Creature
from refuge.models.mixins import FlyingMixin
from refuge.models.species import Dragon, Unicorn, WrongDragon, Phoenix

frostbite = Dragon("Frostbite", "Nordic Realms", 95, "ice")
print([cls.__name__ for cls in Dragon.__mro__])
print(frostbite.travel_mode())
print(frostbite.fly("Frozen Peaks"))
print(frostbite.flight_log)
print(Unicorn("Moonbeam", "Crystal Lake", 67).travel_mode())

print([cls.__name__ for cls in WrongDragon.__mro__])
print(WrongDragon("Test", "Lab", 10, "fire").travel_mode())

print(
    isinstance(frostbite, Creature),
    isinstance(frostbite, FlyingMixin),
    issubclass(Unicorn, FlyingMixin),
    issubclass(Phoenix, Dragon),
)

print(WrongDragon("Test", "Lab", 10, "fire").flight_log)
