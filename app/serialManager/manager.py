import logging
from typing import Tuple
import serial

logger = logging.getLogger(__name__)


class SerialManager:
    def __init__(self, port: str, baudrate: int):
        self.port = port
        self.baudrate = baudrate
        self.connection = None

    def open(self):
        try:
            if self.connection and self.connection.is_open:
                return
            self.connection = serial.Serial(self.port, self.baudrate)
            logger.info(f"Serial port {self.port} opened at {self.baudrate} baud rate.")
        except Exception as e:
            logger.exception("Error during opening serial")
            raise e

    def close(self):
        try:
            if self.connection and self.connection.is_open:
                self.connection.close()
                logger.info(f"Serial port {self.port} closed.")
        except Exception as e:
            logger.exception("Error during opening serial")
            raise e

    def write(self, data: bytes) -> bool:
        try:
            if not self.connection or not self.connection.is_open:
                logger.error(f"Serial port {self.port} is not open.")
                return False
            self.connection.write(data)
            logger.debug(f"Data send to Serial port {self.port}: {data}")
            return data
        except Exception as e:
            logger.exception(f"Error during send data to {self.port}")
            return False

    def read_until(self, expected: bytes) -> Tuple[bool, bytes]:
        try:
            if not self.connection or not self.connection.is_open:
                logger.error(f"Serial port {self.port} is not open.")
                return False
            data_rcv = self.connection.read_until(expected)
            if len(data_rcv) == 0:
                logger.error(
                    f"No data received from Serial port {self.port} with {expected=}"
                )
                return False
            logger.debug(
                f"Data received from Serial port {self.port}: {data_rcv[:50] +b'...' if len(data_rcv)>50 else data_rcv}"
            )
            return data_rcv
        except Exception as e:
            logger.exception(f"Error during send data to {self.port}")
            return False, b""
