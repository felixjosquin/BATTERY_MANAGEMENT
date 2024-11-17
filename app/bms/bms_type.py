from dataclasses import dataclass
from enum import StrEnum, auto
from typing import List


@dataclass
class BMS_ANALOG_VALUE:
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


class BMS_COMMAND(StrEnum):
    GET_ANALOG_VALUE = auto()
