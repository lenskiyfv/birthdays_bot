import os

PG_USER = os.environ["PG_USER"]
PG_PASSWORD = os.environ["PG_PASSWORD"]
PG_HOST = os.getenv("PG_HOST", "db")
PG_PORT = int(os.getenv("PG_PORT", 5432))
PG_DB = os.environ["PG_DB"]
BOT_TOKEN = os.environ["BOT_TOKEN"]

PG_DSN = os.getenv(
    "PG_DSN",
    f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}",
)