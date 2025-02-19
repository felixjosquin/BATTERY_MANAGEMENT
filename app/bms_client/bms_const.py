from typing import Dict, List, Tuple, Type

from pydantic import BaseModel

from app.dto.bms_complete_record import BMS_COMPLETE_RECORD

from .bms_types import BMS_COMMAND, DATA_FORMAT

# Encode Data
CID2_VALUES: Dict[BMS_COMMAND, str] = {
    BMS_COMMAND.GET_ANALOG_VALUE: b"42",
}
EOI = b"\x0d"
SOI = b"\x7e"

# Serial communication
BMS_DEV_REPONSE = {
    b"~22014A42E00201FD28\r": b"~22014A00E0C600168A146D100CC90CC70CC70CC70C9F0CC90CC60CCA0CC60CCB0CC20CC90CC10CC90CC60CC8008C00A000960400AA00AA009600A0FBA400000061013E80241000ED000000020000000000230000000000000000000000000000000000000000000000D3F4\r"
}

# Decode Data
RTN_ERRORS: Dict[bytes, str] = {
    b"00": None,
    b"02": "CHKSUM error",
    b"03": "LCHKSUM error",
    b"04": "CID2 undefined",
    b"09": "Operation or write error",
}

# Extract Data
LENGHT_BYTE_BY_DATA_FORMAT: Dict[DATA_FORMAT, int] = {
    DATA_FORMAT.UNSIGNED_FLOAT: 4,
    DATA_FORMAT.SIGNED_FLOAT: 4,
    DATA_FORMAT.TEMP: 4,
    DATA_FORMAT.INT_2_BYTES: 2,
    DATA_FORMAT.INT_4_BYTES: 4,
}

EXTRACT_DATA_ORDER: Dict[BMS_COMMAND, List[Tuple[str, DATA_FORMAT, Dict]]] = {
    BMS_COMMAND.GET_ANALOG_VALUE: [
        ("soc", DATA_FORMAT.UNSIGNED_FLOAT, {"off": 2}),
        ("batt_volt", DATA_FORMAT.UNSIGNED_FLOAT, {}),
        ("nb_cell", DATA_FORMAT.UNSIGNED_FLOAT, {}),
        ("cells_v", DATA_FORMAT.INT_2_BYTES, {"list": "nb_cell"}),
        ("env_temp", DATA_FORMAT.TEMP, {}),
        ("pack_temp", DATA_FORMAT.TEMP, {}),
        ("mos_temp", DATA_FORMAT.TEMP, {}),
        ("nb_temp", DATA_FORMAT.INT_2_BYTES, {}),
        ("temps", DATA_FORMAT.TEMP, {"list": "nb_temp"}),
        ("current", DATA_FORMAT.SIGNED_FLOAT, {}),
        ("soh", DATA_FORMAT.INT_2_BYTES, {"off": 6}),
        ("full_cap", DATA_FORMAT.SIGNED_FLOAT, {"off": 2}),
        ("remain_cap", DATA_FORMAT.SIGNED_FLOAT, {}),
        ("nb_cycle", DATA_FORMAT.INT_4_BYTES, {}),
    ]
}

RETURN_TYPE: Dict[BMS_COMMAND, Type[BaseModel]] = {
    BMS_COMMAND.GET_ANALOG_VALUE: BMS_COMPLETE_RECORD
}
