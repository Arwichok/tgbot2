import logging
import re

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import aiogram.types as atp
from sqlalchemy.sql.functions import count

from app.database.models import User


async def start_user(session: AsyncSession, from_user: atp.User, deep_link: re.Match):
    user = await session.get(User, from_user.id)
    if user:
        user.is_started = True
        user.name = from_user.first_name
    else:
        user = User(
            id=from_user.id,
            name=from_user.first_name,
            is_started=True,
            refer=int(deep_link.group(1)) if deep_link else None,
        )
        session.add(user)
        logging.info(f"New user {user.name}({user.id})"+(f" ref: {user.refer}" if user.refer else ""))
    return user


async def get_users_count(session: AsyncSession):
    return await session.scalar(count(User.id))
