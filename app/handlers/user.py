import logging
from contextlib import suppress
from typing import Union

import aiogram.types as atp
from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils.exceptions import ChatNotFound

from app.database.models import User
from app.utils.constants import DB


REF_START = "/start r"


async def _filter(obj: Union[atp.Message]):
    return obj.chat.type == atp.ChatType.PRIVATE


async def start_cmd(msg: atp.Message):
    async with msg.bot[DB]() as session:
        if user := await session.get(User, msg.from_user.id):
            user.is_active = True
        else:
            user = User(
                id=msg.from_user.id,
                name=msg.from_user.username,
                fullname=msg.from_user.full_name,
                is_active=True,
            )
            if msg.text.startswith(REF_START):
                with suppress(ChatNotFound):
                    chat = await msg.bot.get_chat(msg.text[len(REF_START) :])
                    if await session.get(User, chat.id):
                        user.refer = chat.id
            session.add(user)
            logging.info(f"New user: {msg.from_user.first_name}({msg.from_user.id})")
        await session.commit()
        return await msg.answer("Welcome!")


async def has_stopped(cmu: atp.ChatMemberUpdated):
    if cmu.new_chat_member.status == atp.ChatMemberStatus.KICKED:
        async with cmu.bot[DB]() as session:
            if user := await session.get(User, cmu.from_user.id):
                user.is_active = False
                await session.commit()
                logging.info(f"User {user.name}({user.id}) stopped bot")


def register(dp: Dispatcher):
    dp.register_message_handler(start_cmd, _filter, CommandStart())
    dp.register_my_chat_member_handler(
        has_stopped, _filter, chat_type=atp.ChatType.PRIVATE
    )
