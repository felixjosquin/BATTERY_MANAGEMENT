from sqlmodel import Session
from app.bms import get_analog_data
from app.bms import SerialManager
from app.database import creat_record
from .custom_exceptions import CustomException


def get_current_data(db: Session, ser: SerialManager):
    sucess, analog_completed_value = get_analog_data(ser)
    if not sucess:
        raise CustomException("Not successfully get analog data")
    creat_record(db, analog_completed_value)
    return analog_completed_value
