from aiogram import Bot, Dispatcher
from aiogram.dispatcher.webhook import BOT_DISPATCHER_KEY
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats, BotCommandScopeChat
from aiohttp import web

from ..database.db import init_db
from .constants import DB
from ..handlers import commands, users, channels, groups, admins
from .config import settings


async def on_startup(dp: Dispatcher):
    admins.register(dp)
    users.register(dp)
    groups.register(dp)
    channels.register(dp)
    commands.register(dp)
    await set_my_commands(dp.bot)
    dp.bot[DB] = await init_db()
    if settings.skip_updates:
        await dp.reset_webhook()
        await dp.skip_updates()


async def on_shutdown(dp: Dispatcher):
    await dp.storage.close()
    await dp.storage.wait_closed()
    await dp.bot.session.close()


async def on_startup_webhook(app: web.Application):
    dp = app[BOT_DISPATCHER_KEY]
    await on_startup(dp)
    await dp.bot.set_webhook(settings.wh_url)


async def on_shutdown_webhook(app: web.Application):
    dp = app[BOT_DISPATCHER_KEY]
    await dp.bot.delete_webhook()
    await on_shutdown(dp)


async def set_my_commands(bot: Bot):
    await bot.set_my_commands(
        [
            BotCommand("start", "Start for Private Chat"),
        ],
        BotCommandScopeAllPrivateChats(),
    )
    await bot.set_my_commands(
        [
            BotCommand("start", "Start for groups"),
        ],
        BotCommandScopeAllGroupChats(),
    )
