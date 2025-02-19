import logging
from typing import Tuple

from app.bms_client.bms_exception import BmsException
from app.config import get_config

from .serial_manager import SerialManager
from .bms_const import RTN_ERRORS, SOI, EOI
from typing import List, Tuple

from .bms_const import EXTRACT_DATA_ORDER, LENGHT_BYTE_BY_DATA_FORMAT, RETURN_TYPE
from .bms_exception import BmsException
from .bms_types import BMS_COMMAND, DATA_FORMAT

logger = logging.getLogger(__name__)
config = get_config()


def bms_encode_data(
    cid2: bytes,
    info: bytes = b"",
    ver: bytes = b"\x32\x32",
    adr: bytes = b"\x30\x31",
    cid1: bytes = b"\x34\x41",
) -> bytes:
    request = SOI
    request += ver
    request += adr
    request += cid1
    if not cid2:
        logger.error(f"Error encode data - No CID2")
        raise BmsException(cause="No CID2", section="Encode data")
    request += cid2
    lenid = bytes(format(len(info), "03X"), "ASCII")
    lchecksum = bytes(lchksum_calc(lenid), "ASCII")
    if not lchecksum:
        logger.error(f"Error encode data - Error calcul LCHEKSUM")
        raise BmsException(cause="Error calcul LCHEKSUM", section="Encode data")
    logger.debug(f"Encode data - calcul {lchecksum=} with {lenid=}")
    request += lchecksum
    request += lenid
    request += info

    checksum = bytes(chksum_calc(request[1:]), "ASCII")
    if not checksum:
        logger.error(f"Error encode data - Error calcul CHEKSUM")
        raise BmsException(cause="Error calcul CHEKSUM", section="Encode data")
    logger.debug(f"Encode data - calcul {checksum=} with {request=}")
    request += checksum
    request += EOI
    return request


def bms_decode_data(inc_data: bytes) -> bytes:
    if len(inc_data) < 14:  # Minimum size
        logger.error(f"Error decode data - Data received too short - {inc_data}")
        raise BmsException(cause="Data received too short", section="Decode data")

    SOI_DATA = inc_data[0:1]
    if SOI_DATA != SOI:
        logger.error(f"Error decode data - Incorrect SOI - {SOI_DATA=}")
        raise BmsException(cause="Incorrect SOI", section="Decode data")

    # VER = inc_data[1:3]
    # ADR = inc_data[3:5]
    # CID1 = inc_data[5:7]
    RTN = inc_data[7:9]
    rtn_error = RTN_ERRORS.get(RTN, "Undefined RTN error")
    if rtn_error:
        logger.warning(f"Error decode data - Incorrect RTN code - {rtn_error}")
        raise BmsException(
            cause=f"Incorrect RTN code - {rtn_error}", section="Decode data"
        )

    LCHKSUM = inc_data[9:10].decode("ASCII")
    LENID = int(inc_data[10:13], 16)
    lchksum_except = lchksum_calc(inc_data[10:13])
    if not lchksum_except or lchksum_except != LCHKSUM:
        logger.warning(
            f"Error decode data - Incorrect LCHKSUM - {lchksum_except=}  {LCHKSUM=}"
        )
        raise BmsException(
            cause=f"Incorrect LCHKSUM - {lchksum_except=}  {LCHKSUM=}",
            section="Decode data",
        )

    INFO = inc_data[13 : 13 + LENID]
    CHKSUM = inc_data[13 + LENID : 13 + LENID + 4].decode("ASCII")
    chksum_except = chksum_calc(inc_data[1:-5])
    if not chksum_except or chksum_except != CHKSUM:
        logger.warning(
            f"Error decode data -  Incorrect CHKSUM - {chksum_except=}  {CHKSUM=}"
        )
        raise BmsException(
            cause=f"Incorrect CHKSUM - {chksum_except=}  {CHKSUM=}",
            section="Decode data",
        )

    logger.debug(
        f"Message decode and validate\n   {RTN=}\n   {LENID=}\n   INFO={INFO[:60]+b'...' if len(INFO)>60 else INFO}"
    )
    return INFO


def bms_extract_data(payload: bytes, command: BMS_COMMAND):
    result = dict()
    offset = 0
    for name, type, config in EXTRACT_DATA_ORDER[command]:
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
    return RETURN_TYPE[command](**result)


def lchksum_calc(lenid: bytes) -> str:
    try:
        chksum = sum([int(chr(bit), 16) for bit in lenid]) % 16
        chksum ^= 0b1111
        chksum += 1
        return format(chksum, "X")
    except Exception as e:
        logger.exception(f"Error calculating LCHKSUM using {lenid=}")
        return ""


def chksum_calc(data: bytes) -> str:
    try:
        chksum = sum(data) % 65536
        chksum ^= 0b1111111111111111
        chksum += 1
        return format(chksum, "X")
    except Exception as e:
        logger.exception(f"Error calculating CHKSUM using {data=}")
        return ""


def extract_value(raw_data, type) -> int | float:
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
