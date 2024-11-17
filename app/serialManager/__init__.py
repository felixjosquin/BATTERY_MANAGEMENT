import logging
from .manager import SerialManager

logger = logging.getLogger(__name__)

if logger.hasHandlers:
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)


__all__ = ["SerialManager"]
