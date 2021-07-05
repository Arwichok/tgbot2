import platform

from aiogram import Dispatcher, types

from app._version import __version__
from app.database.queries import get_users_count
from app.utils.config import settings
from app.utils.constants import DB


async def _filter(msg: types.Message):
    return msg.chat.id in settings.admins


async def info_cmd(msg: types.Message):
    me: types.User = await msg.bot.me
    data = {
        "IP": await (await msg.bot.session.get("https://api.ipify.org/")).text(),
        "PY_VERSION": platform.python_version(),
        "SYSTEM": platform.system(),
        "CAN_JOIN_GROUPS": me.can_join_groups,
        "CAN_READ_ALL_GROUP_MESSAGES": me.can_read_all_group_messages,
        "INLINE_QUERIES": me.supports_inline_queries,
        "MODE": "Webhook" if settings.wh_on else "Polling",
        "BOT_VERSION": __version__,
    }
    text = "<code>" \
           "Bot version: {BOT_VERSION}\n"\
           "IP: {IP}\n" \
           "Namespace: {NAMESPACE_FOR_DYNACONF}\n" \
           "Python: {PY_VERSION}\n" \
           "OS: {SYSTEM}\n" \
           "Join to groups: {CAN_JOIN_GROUPS}\n" \
           "Read all group messages: {CAN_READ_ALL_GROUP_MESSAGES}\n" \
           "Inline mode: {INLINE_QUERIES}\n" \
           "Mode: {MODE}" \
           "</code>"
    await msg.answer(text.format(**data, **settings))


async def users_cmd(msg: types.Message):
    async with msg.bot[DB]() as session:
        count = await get_users_count(session)
        await msg.answer("Users: {}".format(count))


def register(dp: Dispatcher):
    dp.register_message_handler(info_cmd, _filter, commands="info")
    dp.register_message_handler(users_cmd, _filter, commands="users")
