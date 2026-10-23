from refuge.models import Creature

row = {
    "id": 1,
    "name": "Frostbite",
    "species": "Dragon",
    "origin": "Nordic Realms",
    "power_level": 95,
}
frostbite = Creature.from_dict(row)
ember = Creature.from_string("Ember, Phoenix, Ashlands, 72")

print(frostbite)
print(ember.power_level + 1)
print(Creature.is_valid_species("Griffin"), Creature.is_valid_species("Goblin"))
print(Creature.get_total_creatures())

try:
    Creature.from_string("Grub, Goblin, Dark Caves, 12")
except ValueError as error:
    print(error)
