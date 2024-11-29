from sqlmodel import Session, SQLModel, create_engine
from app import get_config


DB_URL = "mysql+pymysql://root:mypassword@localhost:3306/bms"
engine = create_engine(DB_URL, echo=False, pool_recycle=1800, pool_pre_ping=True)

config = get_config()

DB_URL = "mysql+pymysql://root:mypassword@localhost:3306/bms"
engine = create_engine(
    DB_URL, echo=config.ECHO_ENGINE, pool_recycle=1800, pool_pre_ping=True
)


def create_db_and_tables():
    if config.DROP_TABLES_BEFORE_STARTING:
        SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
