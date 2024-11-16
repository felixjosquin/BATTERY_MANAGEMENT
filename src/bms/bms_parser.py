import logging

logger = logging.getLogger(__name__)


def bms_decode_data(inc_data):
    try:
        SOI = hex(ord(inc_data[0:1]))
        if SOI != "0x7e":
            logger.warning(f"Error decode data - Incorrect SOI\n    {SOI=}")

        VER = inc_data[1:3]
        ADR = inc_data[3:5]
        CID1 = inc_data[5:7]
        RTN = inc_data[7:9]
        LCHKSUM = inc_data[9]
        LENID = int(inc_data[10:13], 16)
        chksum_except = lchksum_calc(inc_data[10:13])
        if not chksum_except and chksum_except != LCHKSUM:
            logger.warning(
                f"Error decode data -  Incorrect LCHKSUM\n   {chksum_except=}    {LCHKSUM=}"
            )
        print(ord(chksum_except))
        print(LCHKSUM)
        INFO = inc_data[13 : 13 + LENID]
        CHKSUM = inc_data[13 + LENID : 13 + LENID + 4]
        logger.debug(
            f"Message decode and validate :\n    {ADR=}\n    {RTN=}\n    {LENID=}"
        )
        return INFO
    except Exception as e:
        logger.exception("Error during decode input")


def bms_send_data(inc_data):

    SOI = hex(ord(inc_data[0:1]))
    VER = inc_data[1:3]
    ADR = inc_data[3:5]
    CID1 = inc_data[5:7]
    RTN = inc_data[7:9]
    LCHKSUM = inc_data[9:10]
    LENID = int(inc_data[10:13], 16)
    INFO = inc_data[13 : 13 + LENID]
    CHKSUM = inc_data[13 + LENID : 13 + LENID + 4]
    EOI = inc_data[13 + LENID + 4]
    print("SOI: ", SOI)
    print("VER: ", VER)
    print("ADR: ", ADR)
    print("CID1: ", CID1)
    print("RTN: ", RTN)
    print("LENGTH: ", inc_data[9:13])
    print("LENID: ", LENID)
    print("LCHKSUM: ", LCHKSUM)
    print("INFO: ", INFO)
    print("CHKSUM: ", CHKSUM)
    print("EOI: " + EOI)
    return INFO


def lchksum_calc(lenid: bytes):
    try:
        chksum = sum([int(chr(bit), 16) for bit in lenid]) % 16
        chksum ^= 0b1111
        chksum += 1
        return hex(chksum)[-1].upper()
    except Exception as e:
        logger.exception(f"Error calculating LCHKSUM using {lenid=}")
        return ""
