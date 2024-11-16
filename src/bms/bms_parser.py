import logging
from typing import Tuple

from .bms_const import RTN_ERRORS

logger = logging.getLogger(__name__)


def bms_decode_data(inc_data: bytes) -> Tuple[bool, bytes]:
    try:
        SOI = hex(ord(inc_data[0:1]))
        if SOI != "0x7e":
            logger.warning(f"Error decode data - Incorrect SOI\n    {SOI=}")
            return (False, b"")

        VER = inc_data[1:3]
        ADR = inc_data[3:5]
        CID1 = inc_data[5:7]
        RTN = inc_data[7:9]
        rtn_error = RTN_ERRORS.get(RTN, "Undefined RTN error")
        if rtn_error:
            logger.warning(f"Error decode data - Incorrect RTN code : {rtn_error}")
            return (False, b"")

        LCHKSUM = inc_data[9:10].decode("ASCII")
        LENID = int(inc_data[10:13], 16)
        lchksum_except = lchksum_calc(inc_data[10:13])
        if not lchksum_except or lchksum_except != LCHKSUM:
            logger.warning(
                f"Error decode data -  Incorrect LCHKSUM\n   {lchksum_except=}    {LCHKSUM=}"
            )
            return (False, b"")

        INFO = inc_data[13 : 13 + LENID]
        CHKSUM = inc_data[13 + LENID : 13 + LENID + 4].decode("ASCII")
        chksum_except = chksum_calc(inc_data[1:-5])
        if not chksum_except or chksum_except != CHKSUM:
            logger.warning(
                f"Error decode data -  Incorrect CHKSUM\n   {chksum_except=}    {CHKSUM=}"
            )
            return (False, b"")

        logger.info(
            f"Message decode and validate :\n   {RTN=}\n   {LENID=}\n   INFO={INFO[:60]+b'...' if len(INFO)>60 else INFO}"
        )
        return (False, INFO)

    except Exception as e:
        logger.exception("Error during decode input")
        return (False, b"")


def bms_send_data(inc_data):
    pass


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
