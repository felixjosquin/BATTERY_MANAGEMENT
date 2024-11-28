import logging
from app import get_config
from .bms_api import get_analog_data
from .serial_manager import SerialManager

logger = logging.getLogger(__name__)
config = get_config()

if logger.hasHandlers:
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.setLevel(config.LOGING_LEVEL)

__all__ = ["get_analog_data", "SerialManager"]
