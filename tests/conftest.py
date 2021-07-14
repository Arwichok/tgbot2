import asyncio
import logging
from pathlib import Path

import pytest
import environs
from pyrogram import Client
from tgintegration import BotController


CONFIG_DIR = Path(__file__).parent.parent

env = environs.Env()
env.read_env()


logger = logging.getLogger("tgintegration")
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


@pytest.fixture(scope="session", autouse=True)
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def client():
    client = Client(
        env("SESSION_NAME", "Client"),
        api_id=env.int("API_ID"),
        api_hash=env("API_HASH"),
        workdir=str(CONFIG_DIR),
    )
    await client.start()
    yield client
    await client.stop()


@pytest.fixture(scope="module")
async def controller(client):
    c = BotController(
        client=client,
        peer=env("BOT_TOKEN").split(":")[0],
        max_wait=10.0,
        wait_consecutive=0.8,
    )
    await c.initialize(start_client=False)
    yield c
