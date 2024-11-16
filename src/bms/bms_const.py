RTN_ERRORS: dict[bytes, str] = {
    b"00": None,
    b"02": "CHKSUM error",
    b"03": "LCHKSUM error",
    b"04": "CID2 undefined",
    b"09": "Operation or write error",
}
