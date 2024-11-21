import logging
from .bms_api import getAnologData
from .serialManager import SerialManager
from .bms_type import BMS_ANALOG_VALUE

logger = logging.getLogger(__name__)

if logger.hasHandlers:
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)

__all__ = ["getAnologData", "SerialManager", "BMS_ANALOG_VALUE"]
