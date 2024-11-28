from fastapi import Depends, FastAPI, Request, responses
from contextlib import asynccontextmanager
from typing import Annotated
from sqlmodel import Session

from app.bms import SerialManager
from app.database import get_db, create_db_and_tables
from app.service import CustomException, get_current_data


SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600

serialManager = SerialManager(SERIAL_PORT, BAUD_RATE)


@asynccontextmanager
async def lifespan(app: FastAPI):
    serialManager.open()
    create_db_and_tables()
    yield
    serialManager.close()


app = FastAPI(lifespan=lifespan)


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return responses.JSONResponse(
        status_code=500, content={"message": f"Error occurred - {exc.detail}"}
    )


@app.get("/")
def get_analog_value(db: Annotated[Session, Depends(get_db)]):
    return get_current_data(db, serialManager)
