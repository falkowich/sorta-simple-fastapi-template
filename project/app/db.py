import logging
import os

from fastapi import FastAPI
from tortoise import Tortoise, run_async
from tortoise.contrib.fastapi import register_tortoise

log = logging.getLogger("uvicorn")

DATABASE_URL = os.environ.get("DATABASE_URL")

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


async def generate_schemas() -> None:
    log_row = "Initializing Tortoise..."
    log.info(log_row)
    print(log_row)

    await Tortoise.init(
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["models.tortoise"]},
    )
    log_row = "Generating database schema via Tortoise..."
    log.info(log_row)
    print(log_row)
    await Tortoise.generate_schemas()
    await Tortoise.close_connections()


if __name__ == "__main__":
    run_async(generate_schemas())
