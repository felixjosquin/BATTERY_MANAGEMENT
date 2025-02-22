from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.bms_client import get_analog_data, SerialManager
from app.database import creat_record
from app.database import get_analog_data_between_dates


def get_current_data(db: Session, ser: SerialManager):
    analog_completed_value = get_analog_data(ser)
    creat_record(db, analog_completed_value)
    return analog_completed_value


def get_data_beetween_dates(
    db: Session,
    end_date: datetime,
    start_date: datetime,
):
    end_date = end_date if end_date else datetime.now()
    start_date = start_date if start_date else end_date - timedelta(days=1)
    return get_analog_data_between_dates(db, start_date, end_date)
