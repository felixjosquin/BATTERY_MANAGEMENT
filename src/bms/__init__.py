import logging

from .bms_parser import bms_decode_data, bms_encode_data

logger = logging.getLogger(__name__)

if logger.hasHandlers:
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)

__all__ = ["bms_decode_data", "bms_encode_data"]
