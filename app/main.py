import logging
from datetime import datetime
from fastapi import Depends, FastAPI, Request, responses
from contextlib import asynccontextmanager
from typing import Annotated, Union
from sqlalchemy.orm import Session

from app.bms_client import SerialManager
from app.bms_client.bms_exception import BmsException
from app.database import get_db, create_db_and_tables
from app.service import get_analog_data_between_dates, get_current_data


logger = logging.getLogger(__name__)


SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600

serialManager = SerialManager(SERIAL_PORT, BAUD_RATE)


@asynccontextmanager
async def lifespan():
    serialManager.open()
    create_db_and_tables()
    yield
    serialManager.close()


app = FastAPI(lifespan=lifespan)


@app.exception_handler(BmsException)
def handle_bms_exception(request: Request, exc: BmsException):
    return responses.JSONResponse(
        status_code=500,
        content={
            "detail": str(exc),
        },
    )


@app.get("/")
def get_analog_value(db: Annotated[Session, Depends(get_db)]):
    return get_current_data(db, serialManager)


@app.get("/list")
def get_analog_value(
    db: Annotated[Session, Depends(get_db)],
    end_date: Union[datetime, None] = None,
    start_date: Union[datetime, None] = None,
):
    return get_analog_data_between_dates(db, end_date, start_date)
