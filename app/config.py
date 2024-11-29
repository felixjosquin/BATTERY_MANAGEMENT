import os
import logging


class Config:
    LOGING_LEVEL = logging.ERROR
    SKIP_SERIAL_CALL = False
    DROP_TABLES_BEFORE_STARTING = False
    ECHO_ENGINE = False


class DevelopmentConfig(Config):
    LOGING_LEVEL = logging.DEBUG
    SKIP_SERIAL_CALL = True
    DROP_TABLES_BEFORE_STARTING = True
    ECHO_ENGINE = True


class ProductionConfig(Config):
    LOGING_LEVEL = logging.INFO


def get_config():
    env = os.getenv("ENV", "production").lower()
    if env == "development":
        return DevelopmentConfig()
    return ProductionConfig()
