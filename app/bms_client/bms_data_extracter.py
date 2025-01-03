from enum import Enum, auto
from typing import List, Tuple

from app.bms_client.bms_exception import BmsException


class DATA_FORMAT(Enum):
    UNSIGNED_FLOAT = auto()
    SIGNED_FLOAT = auto()
    TEMP = auto()
    INT_2_BYTES = auto()
    INT_4_BYTES = auto()


LENGHT_BYTE_BY_DATA_FORMAT = {
    DATA_FORMAT.UNSIGNED_FLOAT: 4,
    DATA_FORMAT.SIGNED_FLOAT: 4,
    DATA_FORMAT.TEMP: 4,
    DATA_FORMAT.INT_2_BYTES: 2,
    DATA_FORMAT.INT_4_BYTES: 4,
}


get_data: List[Tuple[str, DATA_FORMAT, dict]] = [
    ("soc", DATA_FORMAT.UNSIGNED_FLOAT, {"off": 2}),
    ("batt_volt", DATA_FORMAT.UNSIGNED_FLOAT, {}),
    ("nb_cell", DATA_FORMAT.UNSIGNED_FLOAT, {}),
    ("cells_v", DATA_FORMAT.INT_2_BYTES, {"list": "nb_cell"}),
    ("env_temp", DATA_FORMAT.TEMP, {}),
    ("pack_temp", DATA_FORMAT.TEMP, {}),
    ("mos_temp", DATA_FORMAT.TEMP, {}),
    ("nb_temp", DATA_FORMAT.INT_2_BYTES, {}),
    ("temps", DATA_FORMAT.TEMP, {"list": "nb_temp"}),
    ("current", DATA_FORMAT.SIGNED_FLOAT, {}),
    ("soh", DATA_FORMAT.INT_2_BYTES, {"off": 6}),
    ("full_cap", DATA_FORMAT.SIGNED_FLOAT, {"off": 2}),
    ("remain_cap", DATA_FORMAT.SIGNED_FLOAT, {}),
    ("nb_cycle", DATA_FORMAT.INT_4_BYTES, {}),
]


def bms_extract_data(payload: bytes):
    result = dict()
    offset = 0
    for name, type, config in get_data:
        offset += config.get("off", 0)
        len_type = LENGHT_BYTE_BY_DATA_FORMAT.get(type)
        if not len_type:
            raise BmsException(section="Extract data", cause=f"Unknow type {type}")
        if config.get("list", False):
            len_list = result.get(config["list"])
            if not len_list:
                raise BmsException(
                    section="Extract data", cause=f"Unknow key {config["list"]}"
                )
            lenght = len_list * len_type
            result[name] = [
                extract_value(payload[offset + i : offset + i + len_type], type)
                for i in range(0, lenght, len_type)
            ]
            offset += lenght
        else:
            result[name] = extract_value(payload[offset : offset + len_type], type)
            offset += len_type
        if offset > len(payload):
            raise BmsException(section="Extract data", cause=f"Payload too short")
    return result


def extract_value(raw_data, type):
    if type == DATA_FORMAT.UNSIGNED_FLOAT:
        return int(raw_data, 16) / 100.0
    elif type == DATA_FORMAT.SIGNED_FLOAT:
        value = int(raw_data, 16)
        if value & (1 << 15):
            value -= 1 << 16
        return value / 100.0
    elif type == DATA_FORMAT.TEMP:
        return int(raw_data, 16) / 10
    elif type == DATA_FORMAT.INT_2_BYTES:
        return int(raw_data, 16)
    elif type == DATA_FORMAT.INT_4_BYTES:
        return int(raw_data, 16)
    else:
        raise BmsException(section="Extract data", cause=f"Unknow {type=}")
