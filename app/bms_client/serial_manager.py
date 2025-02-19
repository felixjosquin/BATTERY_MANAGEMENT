from functools import lru_cache
import logging
import serial
from typing import Tuple

from app import get_config
from app.bms_client.bms_exception import BmsException

from .bms_const import BMS_DEV_REPONSE, EOI

logger = logging.getLogger(__name__)
config = get_config()

SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600


class SerialManager:
    def __init__(self, port: str, baudrate: int):
        self.port = port
        self.baudrate = baudrate
        self.connection = None

    def open(self):
        if config.SKIP_SERIAL_CALL:
            return
        if self.connection and self.connection.is_open:
            return
        self.connection = serial.Serial(self.port, self.baudrate)
        logger.info(f"Serial port {self.port} opened at {self.baudrate} baud rate.")

    def close(self):
        if config.SKIP_SERIAL_CALL:
            return
        if self.connection and self.connection.is_open:
            self.connection.close()
            logger.info(f"Serial port {self.port} closed.")

    def request(self, data_send: bytes) -> bytes:
        if config.SKIP_SERIAL_CALL:
            response = BMS_DEV_REPONSE.get(data_send)
            if not response:
                raise BmsException(
                    section="Serial communication", cause="No response from battery"
                )
            return response
        if not self.connection or not self.connection.is_open:
            raise BmsException(
                section="Serial communication", cause="Serial COM not open"
            )
        self.connection.write(data_send)
        logger.debug(f"Data send to Serial port {self.port}: {data_send}")
        data_rcv = self.connection.read_until(EOI)
        if len(data_rcv) == 0:
            raise BmsException(
                section="Serial communication", cause="No response from battery"
            )
        return data_rcv


@lru_cache
def get_settings():
    return Settings()


serial_manager = SerialManager(SERIAL_PORT, BAUD_RATE)


def open_serial():
    serial_manager.open()


def close_serial():
    serial_manager.close()
