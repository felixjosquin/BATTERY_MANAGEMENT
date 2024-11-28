import logging
from typing import Tuple
from app.config import get_config
from .serial_manager import SerialManager
from .bms_values import RTN_ERRORS, SOI, EOI

logger = logging.getLogger(__name__)
config = get_config()


def bms_request(ser: SerialManager, cid2: bytes, **kwargs) -> Tuple[bool, bytes]:
    try:
        sucess_encode, input = bms_encode_data(cid2, **kwargs)
        if not sucess_encode:
            return False, b""
        print(input)
        sucess_request, response = ser.request(input)
        if not sucess_request:
            return False, b""
        sucess_decode, info = bms_decode_data(response)
        if not sucess_decode:
            return False, b""
        return True, info
    except Exception as e:
        logger.exception("Analog read exception")
        return False


def bms_decode_data(inc_data: bytes) -> Tuple[bool, bytes]:
    try:
        if len(inc_data) < 14:  # Minimum size
            logger.error(f"Error decode data - Data received too short - {inc_data}")
            return (False, b"")

        SOI_DATA = inc_data[0:1]
        if SOI_DATA != SOI:
            logger.error(f"Error decode data - Incorrect SOI\n    {SOI_DATA=}")
            return (False, b"")

        # VER = inc_data[1:3]
        # ADR = inc_data[3:5]
        # CID1 = inc_data[5:7]
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

        logger.debug(
            f"Message decode and validate\n   {RTN=}\n   {LENID=}\n   INFO={INFO[:60]+b'...' if len(INFO)>60 else INFO}"
        )
        return (True, INFO)

    except Exception as e:
        logger.exception("Error during decode data received")
        return (False, b"")


def bms_encode_data(
    cid2: bytes,
    info: bytes = b"",
    ver: bytes = b"\x32\x32",
    adr: bytes = b"\x30\x31",
    cid1: bytes = b"\x34\x41",
) -> Tuple[bool, bytes]:
    request = SOI
    request += ver
    request += adr
    request += cid1
    if not cid2:
        logger.error(f"Error encode data - No CID2")
        return (False, b"")
    request += cid2
    lenid = bytes(format(len(info), "03X"), "ASCII")
    lchecksum = bytes(lchksum_calc(lenid), "ASCII")
    if not lchecksum:
        logger.error(f"Error encode data - Error calcul LCHEKSUM")
        return (False, b"")
    logger.debug(f"Encode data - calcul {lchecksum=} with {lenid=}")
    request += lchecksum
    request += lenid
    request += info

    checksum = bytes(chksum_calc(request[1:]), "ASCII")
    if not checksum:
        logger.error(f"Error encode data - Error calcul CHEKSUM")
        return (False, b"")
    logger.debug(f"Encode data - calcul {checksum=} with {request=}")
    request += checksum
    request += EOI
    return (True, request)


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
