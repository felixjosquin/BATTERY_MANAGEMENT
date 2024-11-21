from sqlmodel import Session

from app.bms import BMS_ANALOG_VALUE
from .model import BMS_Record


def creat_bms_Record(session: Session, data: BMS_ANALOG_VALUE):
    new_record = BMS_Record(
        soc=data.soc,
        batt_volt=data.batt_volt,
        remain_cap=data.remain_cap,
        full_cap=data.full_cap,
        env_temp=data.env_temp,
        pack_temp=data.pack_temp,
        nb_cycle=data.nb_cycle,
    )
    session.add(new_record)
    session.commit()
