import logging
import serial
from typing import Tuple

from app import get_config

from .bms_values import BMS_DEV_REPONSE, EOI

logger = logging.getLogger(__name__)
config = get_config()


class SerialManager:
    def __init__(self, port: str, baudrate: int):
        self.port = port
        self.baudrate = baudrate
        self.connection = None

    def open(self):
        try:
            if config.SKIP_SERIAL_CALL:
                return
            if self.connection and self.connection.is_open:
                return
            self.connection = serial.Serial(self.port, self.baudrate)
            logger.info(f"Serial port {self.port} opened at {self.baudrate} baud rate.")
        except Exception as e:
            logger.exception("Error during opening serial")
            raise e

    def close(self):
        try:
            if config.SKIP_SERIAL_CALL:
                return
            if self.connection and self.connection.is_open:
                self.connection.close()
                logger.info(f"Serial port {self.port} closed.")
        except Exception as e:
            logger.exception("Error during close serial")
            raise e

    def request(self, data_send: bytes) -> Tuple[bool, bytes]:
        try:
            if config.SKIP_SERIAL_CALL:
                response = BMS_DEV_REPONSE.get(data_send)
                return True, response if response else False
            if not self.connection or not self.connection.is_open:
                logger.error(f"Serial port {self.port} is not open.")
                return False
            self.connection.write(data_send)
            logger.debug(f"Data send to Serial port {self.port}: {data_send}")
            data_rcv = self.connection.read_until(EOI)
            if len(data_rcv) == 0:
                logger.error(f"No response from Serial port {self.port}")
                return False
            return True, data_rcv
        except Exception as e:
            logger.exception(f"Error during requesting to {self.port}")
            return False, b""
