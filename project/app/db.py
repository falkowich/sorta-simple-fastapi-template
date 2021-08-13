import logging

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.config import Settings

log = logging.getLogger("uvicorn")
settings = Settings()

DATABASE_URL = settings.database_url

APP_MODELS = ["app.models.tortoise", "aerich.models"]

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": APP_MODELS,
            "default_connection": "default",
        }
    },
}


def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=DATABASE_URL,
        modules={"models": APP_MODELS},
        generate_schemas=False,
        add_exception_handlers=True,
    )
