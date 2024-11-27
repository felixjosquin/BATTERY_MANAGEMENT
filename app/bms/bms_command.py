from dataclasses import dataclass
from enum import StrEnum, auto
from typing import List


class BMS_COMMAND(StrEnum):
    GET_ANALOG_VALUE = auto()
