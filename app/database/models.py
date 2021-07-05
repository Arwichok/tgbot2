from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.sql import expression
from sqlalchemy.sql.functions import now

from .base import Base


class DateTimeBase:
    created_at: datetime = Column(DateTime(True), server_default=now())
    updated_at: datetime = Column(DateTime(True), onupdate=now())


@dataclass
class User(Base, DateTimeBase):
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String)
    refer: int = Column(Integer)
    is_super: bool = Column(Boolean, server_default=expression.false())
    is_started: bool = Column(Boolean, server_default=expression.false())
    is_stopped: bool = Column(Boolean, server_default=expression.false())
