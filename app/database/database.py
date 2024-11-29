from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app import get_config
from .model import Base

config = get_config()

DB_URL = "mysql+pymysql://root:mypassword@localhost:3306/bms"
engine = create_engine(
    DB_URL, echo=config.ECHO_ENGINE, pool_recycle=1800, pool_pre_ping=True
)


def create_db_and_tables():
    if config.DROP_TABLES_BEFORE_STARTING:
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
