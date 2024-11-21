from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends, FastAPI
from sqlmodel import Session
from app.bms import getAnologData, SerialManager
from app.database import creat_bms_Record, get_db, create_db_and_tables


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


@app.get("/")
def get_analog_value(db: Annotated[Session, Depends(get_db)]):
    sucess, analogValue = getAnologData(serialManager)
    creat_bms_Record(db, analogValue)
    return analogValue.__dict__
