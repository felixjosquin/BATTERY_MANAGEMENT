from enum import Enum, auto
from typing import List, Tuple

from app.bms_client.bms_exception import BmsException


class PayloadType(Enum):
    UNSIGNED_FLOAT = auto()
    SIGNED_FLOAT = auto()
    TEMP = auto()
    INT_2_BYTES = auto()
    INT_4_BYTES = auto()


lenght_payload_type = {
    PayloadType.UNSIGNED_FLOAT: 4,
    PayloadType.SIGNED_FLOAT: 4,
    PayloadType.TEMP: 4,
    PayloadType.INT_2_BYTES: 2,
    PayloadType.INT_4_BYTES: 4,
}


get_data: List[Tuple[str, PayloadType, dict]] = [
    ("soc", PayloadType.UNSIGNED_FLOAT, {"off": 2}),
    ("batt_volt", PayloadType.UNSIGNED_FLOAT, {}),
    ("nb_cell", PayloadType.UNSIGNED_FLOAT, {}),
    ("cells_v", PayloadType.INT_2_BYTES, {"list": "nb_cell"}),
    ("env_temp", PayloadType.TEMP, {}),
    ("pack_temp", PayloadType.TEMP, {}),
    ("mos_temp", PayloadType.TEMP, {}),
    ("nb_temp", PayloadType.INT_2_BYTES, {}),
    ("temps", PayloadType.TEMP, {"list": "nb_temp"}),
    ("current", PayloadType.SIGNED_FLOAT, {}),
    ("soh", PayloadType.INT_2_BYTES, {"off": 6}),
    ("full_cap", PayloadType.SIGNED_FLOAT, {"off": 2}),
    ("remain_cap", PayloadType.SIGNED_FLOAT, {}),
    ("nb_cycle", PayloadType.INT_4_BYTES, {}),
]


def bms_extract_data(payload: bytes):
    result = dict()
    offset = 0
    for name, type, config in get_data:
        offset += config.get("off", 0)
        len_type = lenght_payload_type.get(type)
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


def extract_value(raw_data, type):
    if type == PayloadType.UNSIGNED_FLOAT:
        return int(raw_data, 16) / 100.0
    elif type == PayloadType.SIGNED_FLOAT:
        value = int(raw_data, 16)
        if value & (1 << 15):
            value -= 1 << 16
        return value / 100.0
    elif type == PayloadType.TEMP:
        return int(raw_data, 16) / 10
    elif type == PayloadType.INT_2_BYTES:
        return int(raw_data, 16)
    elif type == PayloadType.INT_4_BYTES:
        return int(raw_data, 16)
    else:
        raise BmsException(section="Extract data", cause=f"Unknow {type=}")
