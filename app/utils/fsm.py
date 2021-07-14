from dataclasses import asdict

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage

from app.utils.config import settings


def init_storage():
    if settings.use_redis:
        storage = RedisStorage(**asdict(settings.redis))
    else:
        storage = MemoryStorage()
    return storage
