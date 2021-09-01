import asyncio
import json
import logging
import os
from uuid import UUID

import pytest
from tortoise import Tortoise

import scripts.manage as manage
from app.config import Settings
from app.models.user import User

log = logging.getLogger("uvicorn")

settings = Settings(testing=1, database_url=os.environ.get("DATABASE_TEST_URL"))

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


async def delete_testadmin() -> None:

    await Tortoise.init(
        db_url=settings.database_url,
        modules={"models": APP_MODELS},
    )
    await User.filter(username="testadmin").delete()
    await Tortoise.close_connections()


def is_valid_uuid(uuid_str):
    uuid_split = uuid_str.split("Password: ")
    uuid_str = uuid_split[1][:-1]
    try:
        UUID(uuid_str, version=4)
        return True
    except ValueError:
        return False


@pytest.mark.asyncio
async def test_show_settings(capsys):
    await manage.show_settings(settings)
    captured = capsys.readouterr()
    assert "testing=True" in captured.out


@pytest.mark.asyncio
async def test_create_admin(capsys):
    await manage.create_admin(settings, True)
    captured = capsys.readouterr()
    assert "User: admin" in captured.out
    assert is_valid_uuid(captured.out)
    await manage.create_admin(settings, True)
    await delete_testadmin()


@pytest.mark.asyncio
async def test_create_admin_when_already_created(capsys):
    await manage.create_admin(settings, True)
    await manage.create_admin(settings, True)
    captured = capsys.readouterr()
    assert "Administrator already created" in captured.out
    await delete_testadmin()


@pytest.mark.asyncio
async def test_generate_schemas(capsys):
    await manage.generate_schemas(log, settings)
    captured = capsys.readouterr()
    assert "Generating database schema via Tortoise" in captured.out
