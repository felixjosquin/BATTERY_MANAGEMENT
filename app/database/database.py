from sqlmodel import Session, SQLModel, create_engine

DB_URL = "mysql+pymysql://root:mypassword@localhost:3306/bms"
engine = create_engine(DB_URL, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
