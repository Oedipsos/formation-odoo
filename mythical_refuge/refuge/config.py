import os

from dotenv import load_dotenv


def db_settings(dbname: str | None = None) -> dict[str, str]:
    load_dotenv()

    settings = {}
    settings["host"] = os.getenv("DB_HOST", "localhost")
    settings["port"] = os.getenv("DB_PORT", "5432")
    settings["dbname"] = dbname or os.environ["DB_NAME"]
    settings["user"] = os.environ["DB_USER"]
    settings["password"] = os.environ["DB_PASSWORD"]

    return settings
