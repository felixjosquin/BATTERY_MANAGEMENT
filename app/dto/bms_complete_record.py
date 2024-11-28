from typing import List
from pydantic import BaseModel


class BMS_COMPLETE_RECORD(BaseModel):
    soc: float = None
    batt_volt: float = None
    cells_v: List[float] = None
    temp: List[int] = None
    env_temp: int = None
    pack_temp: int = None
    mos_temp: int = None
    current: float = None
    soh: int = None
    full_cap: float = None
    remain_cap: float = None
    nb_cycle: int = None
