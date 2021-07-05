import asyncio
import logging
from pathlib import Path

import pytest
from dynaconf import Dynaconf
from pyrogram import Client
from tgintegration import BotController


CONFIG_DIR = Path(__file__).parent.parent / "config"

settings = Dynaconf(
    envvar_prefix=False,
    environments=True,
    settings_files=["settings.toml", ".secrets.toml", "settings.local.toml"],
)

logger = logging.getLogger("tgintegration")
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


@pytest.fixture(scope="session", autouse=True)
def event_loop(_):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def client():
    client = Client(
        "UserBot",
        api_id=settings.api_id,
        api_hash=settings.api_hash,
        workdir=str(CONFIG_DIR),
    )
    await client.start()
    yield client
    await client.stop()


@pytest.fixture(scope="module")
async def controller(client):
    c = BotController(
        client=client,
        peer=settings.bot_token.split(":")[0],
        max_wait=10.0,
        wait_consecutive=0.8,
    )
    await c.initialize(start_client=False)
    yield c
