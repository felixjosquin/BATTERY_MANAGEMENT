import logging
from app.dto import BMS_COMPLETE_RECORD

from typing import Tuple
from .bms_const import CID2_VALUES
from .bms_parser import bms_request
from .serial_manager import SerialManager
from .bms_command import BMS_COMMAND

logger = logging.getLogger(__name__)


def get_analog_data(ser: SerialManager) -> Tuple[bool, BMS_COMPLETE_RECORD]:

    sucess, info = bms_request(
        ser=ser,
        cid2=CID2_VALUES[BMS_COMMAND.GET_ANALOG_VALUE],
        info=b"01",
    )

    if not sucess:
        return False

    analog_value = BMS_COMPLETE_RECORD()

    byte_index = 2
    analog_value.soc = int(info[byte_index : byte_index + 4], 16) / 100.0
    byte_index += 4

    analog_value.batt_volt = int(info[byte_index : byte_index + 4], 16) / 100.0
    byte_index += 4

    nb_cells = int(info[byte_index : byte_index + 2], 16)
    byte_index += 2

    analog_value.cells_v = [
        int(info[byte_index + 4 * i : byte_index + 4 * (i + 1)], 16)
        for i in range(nb_cells)
    ]
    byte_index += 4 * nb_cells

    analog_value.env_temp = int(info[byte_index : byte_index + 4], 16) / 10.0
    byte_index += 4
    analog_value.pack_temp = int(info[byte_index : byte_index + 4], 16) / 10.0
    byte_index += 4
    analog_value.mos_temp = int(info[byte_index : byte_index + 4], 16) / 10.0
    byte_index += 4

    nb_temp = int(info[byte_index : byte_index + 2], 16)
    byte_index += 2

    analog_value.temp = [
        int(info[byte_index + 4 * i : byte_index + 4 * (i + 1)], 16) / 10.0
        for i in range(nb_temp)
    ]
    byte_index += 4 * nb_temp

    analog_value.current = get_unsigned_value(info[byte_index : byte_index + 4]) / 100.0
    byte_index += 4

    byte_index += 6

    analog_value.soh = int(info[byte_index : byte_index + 2], 16)
    byte_index += 2

    byte_index += 2

    analog_value.full_cap = int(info[byte_index : byte_index + 4], 16) / 100.0
    byte_index += 4

    analog_value.remain_cap = int(info[byte_index : byte_index + 4], 16) / 100.0
    byte_index += 4

    analog_value.nb_cycle = int(info[byte_index : byte_index + 4], 16)
    byte_index += 4

    logger.info(
        f"Analog Data received and decode   SOC: {analog_value.soc} %   Battery Voltage: {analog_value.batt_volt} V   Current: {analog_value.current} A"
    )

    return True, analog_value


def get_unsigned_value(hexstr):
    value = int(hexstr, 16)
    if value & (1 << 15):
        value -= 1 << 16
    return value
