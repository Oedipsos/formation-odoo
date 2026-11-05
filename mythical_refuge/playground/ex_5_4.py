from refuge.db.connection import DatabaseConnection
from refuge.exceptions import NotFoundError
from refuge.models.species import Dragon, Phoenix
from refuge.models.species import Phoenix
from refuge.repositories.protocols import CreatureRepository
from refuge.repositories.postgres import PostgresCreatureRepository
from refuge.repositories.in_memory import InMemoryCreatureRepository


def describe_refuge(repo: CreatureRepository) -> None:
    creatures = repo.list_all()
    n = len(creatures)
    names = ", ".join(c.name for c in creatures)
    print(n, "creature(s):", names)


with DatabaseConnection() as db:
    repo = PostgresCreatureRepository(db)
    for creature in repo.list_all():
        print(creature)
    ember = repo.get("Ember")
    print(repr(ember), ember.resurrection_count)

    with db.transaction():
        cinder = repo.add(Dragon("Cinder", "Ashlands", 60, "fire"))
    print(cinder.id)

    try:
        repo.get("Grub")
    except NotFoundError as error:
        print(error)

memory = InMemoryCreatureRepository()
memory.add(Phoenix("Ember", "Ashlands", 72))
memory.add(Dragon("Frostbite", "Nordic Realms", 95, "ice"))
describe_refuge(memory)
