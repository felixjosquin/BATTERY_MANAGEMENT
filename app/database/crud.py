from sqlmodel import Session

from app.dto import BMS_COMPLETE_RECORD
from app.dto import BMS_ESSENTIAL_RECORD
from .model import ANALOG_RECORD


def creat_record(session: Session, data: BMS_COMPLETE_RECORD):
    new_record = ANALOG_RECORD(**data.model_dump())
    session.add(new_record)
    session.commit()
    session.refresh(new_record)
    return BMS_ESSENTIAL_RECORD(**new_record.__dict__)
