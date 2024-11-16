from enum import Enum

EOI = b"\x0d"
SOI = b"\x7e"
RTN_ERRORS: dict[bytes, str] = {
    b"00": None,
    b"02": "CHKSUM error",
    b"03": "LCHKSUM error",
    b"04": "CID2 undefined",
    b"09": "Operation or write error",
}


class CID2_VALUES(Enum):
    ANALOG_VALUE = b"42"
