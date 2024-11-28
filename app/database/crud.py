import pytz
from datetime import datetime
from typing import List
from sqlmodel import Session, select

from app.dto import BMS_COMPLETE_RECORD, BMS_ESSENTIAL_RECORD

from .model import ANALOG_RECORD


def creat_record(session: Session, data: BMS_COMPLETE_RECORD) -> BMS_ESSENTIAL_RECORD:
    new_record = ANALOG_RECORD(**data.model_dump())
    session.add(new_record)
    session.commit()
    session.refresh(new_record)
    return BMS_ESSENTIAL_RECORD(**new_record.model_dump())


def get_analog_data_between_dates(
    session: Session, start_date: datetime, end_date: datetime
) -> List[BMS_ESSENTIAL_RECORD]:
    query = (
        select(ANALOG_RECORD)
        .where(ANALOG_RECORD.created_at >= start_date.astimezone(tz=pytz.UTC))
        .where(ANALOG_RECORD.created_at <= end_date.astimezone(tz=pytz.UTC))
    )
    results = session.exec(query).all()
    return [BMS_ESSENTIAL_RECORD(**record.model_dump()) for record in results]
