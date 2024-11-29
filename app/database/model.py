import pytz
from datetime import datetime
from typing import Optional
from sqlalchemy import Float, Integer, Numeric, func, Column
from sqlalchemy.types import TypeDecorator, DateTime
from sqlalchemy.orm import DeclarativeBase


class DateTimeWithTz(TypeDecorator):
    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return value

    def process_result_value(self, value: Optional[datetime], dialect):
        if value is None:
            return value
        return pytz.UTC.localize(value).astimezone(pytz.timezone("Europe/Paris"))


class Base(DeclarativeBase):
    pass


class ANALOG_RECORDS(Base):

    __tablename__ = "analog_records"

    id = Column(Integer, primary_key=True)
    soc = Column(Float, default=0)
    current = Column(Float, default=0)
    batt_volt = Column(Float, default=0)
    remain_cap = Column(Float, default=0)
    full_cap = Column(Float, default=0)
    env_temp = Column(Integer, default=0)
    pack_temp = Column(Integer, default=0)
    nb_cycle = Column(Integer, default=0)
    soh = Column(Integer, default=0)
    created_at = Column(type_=DateTimeWithTz, server_default=func.now())

    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
