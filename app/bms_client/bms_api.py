import logging

from app.dto import BMS_COMPLETE_RECORD

from .bms_const import CID2_VALUES, BMS_COMMAND
from .bms_parser import bms_decode_data, bms_encode_data, bms_extract_data
from .serial_manager import SerialManager
from .bms_exception import BmsException

logger = logging.getLogger(__name__)


def request_bms(serialManager: SerialManager, bms_command: BMS_COMMAND):
    try:
        section = "Decode data"
        cid2 = CID2_VALUES[bms_command]
        input = bms_encode_data(cid2)
        section = "Serial communication"
        response = serialManager.request(input)
        section = "Decode data"
        payload = bms_decode_data(response)
        section = "Extract data"
        return bms_extract_data(payload, bms_command)
    except BmsException:
        raise
    except Exception as e:
        raise BmsException(section=section, cause=f"Uncatch error : {e}")


def get_analog_data(serialManager) -> BMS_COMPLETE_RECORD:
    return request_bms(serialManager, BMS_COMMAND.GET_ANALOG_VALUE)
