from sqlmodel import Session
from app.bms import get_analog_data, SerialManager
from app.database import creat_record
from .custom_exceptions import CustomException


def get_current_data(db: Session, ser: SerialManager):
    sucess, analog_completed_value = get_analog_data(ser)
    if not sucess:
        raise CustomException("Not successfully get analog data")
    a = creat_record(db, analog_completed_value)
    return a
