import logging
from app.bms import SerialManager

from typing import Tuple
from .bms_const import CID2_VALUES, EOI
from .bms_parser import bms_encode_data, bms_decode_data
from .bms_type import BMS_ANALOG_VALUE, BMS_COMMAND


logger = logging.getLogger(__name__)


def getAnologData(ser: SerialManager) -> Tuple[bool, BMS_ANALOG_VALUE]:
    try:
        sucess_encode, input = bms_encode_data(
            CID2_VALUES[BMS_COMMAND.GET_ANALOG_VALUE], b"01"
        )
        if not sucess_encode:
            return False
        logger.info(f"message to get analogData send - {input}")
        ser.write(input)
        response = ser.read_until(EOI)
        if not response:
            logger.warning(f"No reponse from battery with input: {input}")
            return False
        sucess_decode, info = bms_decode_data(response)
        if not sucess_decode:
            return False

        analog_value = BMS_ANALOG_VALUE()

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

        analog_value.env_temp = int(info[byte_index : byte_index + 4], 16) / 10
        byte_index += 4
        analog_value.pack_temp = int(info[byte_index : byte_index + 4], 16) / 10
        byte_index += 4
        analog_value.mos_temp = int(info[byte_index : byte_index + 4], 16) / 10
        byte_index += 4

        nb_temp = int(info[byte_index : byte_index + 2], 16)
        byte_index += 2

        analog_value.temp = [
            int(info[byte_index + 4 * i : byte_index + 4 * (i + 1)], 16) / 10
            for i in range(nb_temp)
        ]
        byte_index += 4 * nb_temp

        analog_value.current = (
            get_unsigned_value(info[byte_index : byte_index + 4]) / 100
        )
        byte_index += 4

        byte_index += 6

        analog_value.soh = int(info[byte_index : byte_index + 2], 16)
        byte_index += 2

        byte_index += 2

        analog_value.full_cap = int(info[byte_index : byte_index + 4], 16) / 100
        byte_index += 4

        analog_value.remain_cap = int(info[byte_index : byte_index + 4], 16) / 100
        byte_index += 4

        analog_value.nb_cycle = int(info[byte_index : byte_index + 4], 16)
        byte_index += 4

        logger.info(
            f"Analog Data received and decode\n    SOC: {analog_value.soc} %\n    Battery Voltage: {analog_value.batt_volt} V\n    Current: {analog_value.current} A"
        )

        return (True, analog_value)

    except Exception as e:
        logger.exception("Analog read exception")
        return False


def get_unsigned_value(hexstr):
    value = int(hexstr, 16)
    if value & (1 << 15):
        value -= 1 << 16
    return value
