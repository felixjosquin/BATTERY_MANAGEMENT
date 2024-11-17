from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.serialManager import SerialManager
from app.bms import getAnologData

SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600

serialManager = SerialManager(SERIAL_PORT, BAUD_RATE)


@asynccontextmanager
async def lifespan(app: FastAPI):
    serialManager.open()
    yield
    serialManager.close()


app = FastAPI(lifespan=lifespan)


@app.get("/analog_value")
def get_analog_value():
    sucess, analogValue = getAnologData(serialManager)
    return analogValue.__dict__
