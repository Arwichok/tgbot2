from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count

from app.database.models import User


async def get_users_count(session: AsyncSession):
    return await session.scalar(count(User.id))
