import pytest

pytestmark = pytest.mark.asyncio


async def test_start(controller, client):
    async with controller.collect(count=1) as res:
        await controller.send_command("/start")

    assert res.num_messages == 1
    assert res[0].text
