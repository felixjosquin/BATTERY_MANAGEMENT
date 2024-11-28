from dataclasses import dataclass
from typing import List


@dataclass
class BMS_COMPLETE_RECORD:
    soc: float = None
    batt_volt: float = None
    cells_v: List[float] = None
    temp: List[int] = None
    env_temp: int = None
    pack_temp: int = None
    mos_temp: int = None
    current: float = None
    soh: int = None
    full_cap: int = None
    remain_cap: int = None
    nb_cycle: int = None
