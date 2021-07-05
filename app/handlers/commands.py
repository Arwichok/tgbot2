import time
import datetime

from aiogram import Dispatcher, types as atp
from aiogram.dispatcher.filters import CommandStart, CommandHelp

from app.database.models import User
from app.utils.constants import START_TIME


async def start_cmd(msg: atp.Message):
    await msg.answer(f"Hello {msg.from_user.first_name} in {msg.chat.title}")


async def help_cmd(msg: atp.Message):
    await msg.answer(f"Help {datetime.timedelta(seconds=int(time.time() - START_TIME))}")


async def stop_handler(cmu: atp.ChatMemberUpdated):
    if cmu.new_chat_member.status == atp.ChatMemberStatus.KICKED:
        await User.stopped(cmu.bot['db'], cmu.from_user)


def register(dp: Dispatcher):
    dp.register_message_handler(start_cmd, CommandStart())
    dp.register_message_handler(help_cmd, CommandHelp())
