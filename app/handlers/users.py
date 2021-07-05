import logging
import re
from typing import Union

import aiogram.types as atp
from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart

from app.database.models import User
from app.database.queries import start_user
from app.utils.constants import DB


async def _filter(obj: Union[atp.Message]):
    return obj.chat.type == atp.ChatType.PRIVATE


async def start_cmd(msg: atp.Message, deep_link: re.Match = None):
    async with msg.bot[DB]() as session:
        user = await start_user(session, msg.from_user, deep_link)
        await msg.answer(f"Hello {msg.from_user.first_name}! {user.refer or ''}")
        await session.commit()


async def help_cmd(msg: atp.Message):
    await msg.answer("Help")


async def has_stopped(cmu: atp.ChatMemberUpdated):
    if cmu.new_chat_member.status == atp.ChatMemberStatus.KICKED:
        async with cmu.bot[DB]() as session:
            if user := await session.get(User, cmu.from_user.id):
                user.is_stopped = True
                await session.commit()
                logging.info(f"User {user.name}({user.id}) stopped bot")


def register(dp: Dispatcher):
    dp.register_message_handler(start_cmd, _filter, CommandStart(re.compile(r'ref([\d]+)')) | CommandStart())
    dp.register_my_chat_member_handler(has_stopped, _filter, chat_type=atp.ChatType.PRIVATE)
