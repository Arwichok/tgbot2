import asyncio
import logging
from contextlib import suppress
from logging import DEBUG, INFO

from aiogram import Bot, Dispatcher, types
from aiogram.bot.api import TelegramAPIServer
from aiogram.dispatcher.webhook import (BOT_DISPATCHER_KEY,
                                        WebhookRequestHandler)
from aiohttp import BasicAuth, web

from app.states.storage import init_storage
from app.utils.config import settings
from app.utils.events import on_shutdown, on_shutdown_webhook, on_startup, on_startup_webhook


def init_dispatcher():
    bot = Bot(
        token=settings.bot_token,
        parse_mode=types.ParseMode.HTML,
        proxy=settings.proxy,
        proxy_auth=BasicAuth(**settings.proxy_auth),
        server=TelegramAPIServer.from_base(settings.tg_api),
    )
    return Dispatcher(bot, storage=init_storage())


async def polling():
    dp = init_dispatcher()
    try:
        await on_startup(dp)
        await dp.start_polling(**settings.polling)
    finally:
        await on_shutdown(dp)


async def webhook() -> web.Application:
    app: web.Application = web.Application()
    app["_check_ip"] = settings.check_ip
    app[BOT_DISPATCHER_KEY] = init_dispatcher()
    app.router.add_route("*", settings.path, WebhookRequestHandler)
    app.on_startup.append(on_startup_webhook)
    app.on_shutdown.append(on_shutdown_webhook)
    return app


def run():
    logging.basicConfig(level=DEBUG if settings.debug else INFO)
    if settings.wh_on:
        web.run_app(webhook(), **settings.server)
    else:
        with suppress(KeyboardInterrupt, SystemExit):
            asyncio.run(polling())
