from refuge.models.creature import Creature

frostbite = Creature("Frostbite", "Dragon", "Nordic Realms", 95)
ember = Creature("Ember", "Phoenix", "Ashlands", 72)

print(frostbite)
frostbite.send_on_mission()
print(frostbite)
frostbite.return_to_refuge()
print(Creature._total_creatures)
