from sqlmodel import Session

from app.dto import BMS_COMPLETE_RECORD
from .model import BMS_Record


def creat_record(session: Session, data: BMS_COMPLETE_RECORD):
    new_record = BMS_Record(
        soc=data.soc,
        current=data.current,
        batt_volt=data.batt_volt,
        remain_cap=data.remain_cap,
        full_cap=data.full_cap,
        env_temp=data.env_temp,
        pack_temp=data.pack_temp,
        nb_cycle=data.nb_cycle,
    )
    session.add(new_record)
    session.commit()
