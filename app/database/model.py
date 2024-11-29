import pytz
from decimal import Decimal
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import func, Column
from sqlalchemy.types import TypeDecorator, DateTime


class DateTimeWithTz(TypeDecorator):
    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return value

    def process_result_value(self, value: Optional[datetime], dialect):
        if value is None:
            return value
        return pytz.UTC.localize(value).astimezone(pytz.timezone("Europe/Paris"))


class ANALOG_RECORD(SQLModel, table=True):

    __tablename__ = "analog_record"

    id: int | None = Field(default=None, primary_key=True)
    soc: Decimal = Field(default=0, max_digits=5, decimal_places=2)
    current: Decimal = Field(default=0, max_digits=4, decimal_places=2)
    batt_volt: Decimal = Field(default=0, max_digits=4, decimal_places=2)
    remain_cap: Decimal = Field(default=0, max_digits=5, decimal_places=2)
    full_cap: Decimal = Field(default=0, max_digits=5, decimal_places=2)
    env_temp: int = Field(default=0, max_digits=3, decimal_places=1)
    pack_temp: int = Field(default=0, max_digits=3, decimal_places=1)
    nb_cycle: int = Field(default=0)
    soh: int = Field(default=0)
    created_at: datetime = Field(
        default=None,
        sa_column=Column(type_=DateTimeWithTz, server_default=func.now()),
    )


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
