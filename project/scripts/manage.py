import sys

sys.path.append("/usr/src/app/")
import argparse
import asyncio
import logging
import uuid

from tortoise import Tortoise
from tortoise.exceptions import IntegrityError

from app.config import Settings
from app.core import get_password_hash
from app.models.user import User

log = logging.getLogger("uvicorn")
settings = Settings()

DATABASE_URL = settings.database_url

APP_MODELS = ["app.models.user", "aerich.models"]

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": APP_MODELS,
            "default_connection": "default",
        }
    },
}

MODE_CHOICES = ["show-settings", "create-admin", "generate-schemas"]


async def generate_schemas(log, settings) -> None:
    log_row = "Initializing Tortoise..."
    log.info(log_row)
    print(log_row)
    await Tortoise.init(
        db_url=settings.database_url,
        modules={"models": APP_MODELS},
    )
    log_row = "Generating database schema via Tortoise..."
    log.info(log_row)
    print(log_row)
    await Tortoise.generate_schemas()
    await Tortoise.close_connections()


async def create_admin(settings, test=False) -> None:
    plain_password = str(uuid.uuid4())
    hashed_password = await get_password_hash(plain_password)

    if test:
        username = "testadmin"
    else:
        username = "admin"

    await Tortoise.init(
        db_url=settings.database_url,
        modules={"models": APP_MODELS},
    )
    user = User(
        username=username,
        email="admin@example.com",
        full_name="Builtin Administratior",
        disabled=False,
        hashed_password=hashed_password,
    )
    try:
        await user.save()
        print("User: admin")
        print(
            f"Password: {plain_password}"
        )  # lgtm [py/clear-text-logging-sensitive-data ]
    except IntegrityError as error:
        print("Administrator already created")

    await Tortoise.close_connections()


async def show_settings(settings):
    print(settings)


async def main():

    parser = argparse.ArgumentParser(description="An argparse example")
    parser.add_argument(
        "--mode",
        "-m",
        choices=MODE_CHOICES,
        help="The action to take (e.g. install, remove, etc.)",
    )
    args = parser.parse_args()

    if args.mode == "show-settings":
        await show_settings(settings)
    elif args.mode == "generate-schemas":
        await generate_schemas(log, settings)
    elif args.mode == "create-admin":
        await create_admin(settings, False)
    else:
        print("whet?")


if __name__ == "__main__":
    asyncio.run(main())
