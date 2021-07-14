from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.sql import expression
from sqlalchemy.sql.functions import now

from .base import Base


class DateTimeBase:
    created_at: datetime = Column(DateTime(True), server_default=now())
    updated_at: datetime = Column(DateTime(True), onupdate=now())


@dataclass
class User(Base, DateTimeBase):
    __tablename__ = "users"
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String)
    fullname: str = Column(String)
    is_active: bool = Column(Boolean, server_default=expression.false())
    refer: Optional[int] = Column(Integer)
