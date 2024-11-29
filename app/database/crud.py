import pytz
from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.dto import BMS_COMPLETE_RECORD, BMS_ESSENTIAL_RECORD
from .model import ANALOG_RECORDS


def creat_record(session: Session, data: BMS_COMPLETE_RECORD) -> BMS_ESSENTIAL_RECORD:
    new_record = ANALOG_RECORDS(**data.model_dump())
    session.add(new_record)
    session.commit()
    session.refresh(new_record)
    return new_record


def get_analog_data_between_dates(
    session: Session, start_date: datetime, end_date: datetime
) -> List[BMS_ESSENTIAL_RECORD]:
    query = (
        select(ANALOG_RECORDS)
        .where(ANALOG_RECORDS.created_at >= start_date.astimezone(tz=pytz.UTC))
        .where(ANALOG_RECORDS.created_at <= end_date.astimezone(tz=pytz.UTC))
    )
    results = session.scalars(query).all()
    return [BMS_ESSENTIAL_RECORD(**record.__dict__) for record in results]
