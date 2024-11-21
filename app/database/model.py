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
        return pytz.UTC.localize(value)


class BMS_Record(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    soc: Decimal = Field(default=0, max_digits=5, decimal_places=2)
    batt_volt: Decimal = Field(default=0, max_digits=4, decimal_places=2)
    remain_cap: Decimal = Field(default=0, max_digits=5, decimal_places=2)
    full_cap: Decimal = Field(default=0, max_digits=5, decimal_places=2)
    env_temp: Decimal = Field(default=0, max_digits=3, decimal_places=1)
    pack_temp: Decimal = Field(default=0, max_digits=3, decimal_places=1)
    nb_cycle: int = Field(default=0, max_digits=3, decimal_places=1)
    created_at: datetime = Field(
        default=None,
        sa_column=Column(type_=DateTimeWithTz, server_default=func.now()),
    )
