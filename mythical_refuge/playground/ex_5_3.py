from refuge.db.connection import DatabaseConnection

with DatabaseConnection() as db:
    with db.cursor() as cur:
        cur.execute("SELECT COUNT(*) AS n FROM creatures")
        print(cur.fetchone()["n"])
        cur.execute(
            "SELECT name, power_level FROM creatures WHERE species = %s ORDER BY name",
            ("Dragon",),
        )
        print([dict(row) for row in cur.fetchall()])
    try:
        with db.transaction():
            with db.cursor() as cur:
                cur.execute(
                    "UPDATE creatures SET power_level = power_level + 1 WHERE name = %s",
                    ("Ignis",),
                )
                raise RuntimeError("Dispatch system failure!")
    except RuntimeError as error:
        print("Rolled back:", error)

    with db.cursor() as cur:
        cur.execute("SELECT power_level FROM creatures WHERE name = %s", ("Ignis",))
        print(cur.fetchone()["power_level"])

try:
    db.cursor()
except RuntimeError as error:
    print(error)
