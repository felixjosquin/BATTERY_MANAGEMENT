from pydantic import BaseModel
from datetime import datetime


class BMS_ESSENTIAL_RECORD(BaseModel):
    soc: float
    current: float
    batt_volt: float
    remain_cap: float
    full_cap: float
    env_temp: int
    pack_temp: int
    nb_cycle: int
    soh: int
    created_at: datetime
