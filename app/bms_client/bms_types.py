from enum import StrEnum, auto


class BMS_COMMAND(StrEnum):
    GET_ANALOG_VALUE = auto()


class DATA_FORMAT(StrEnum):
    UNSIGNED_FLOAT = auto()
    SIGNED_FLOAT = auto()
    TEMP = auto()
    INT_2_BYTES = auto()
    INT_4_BYTES = auto()
