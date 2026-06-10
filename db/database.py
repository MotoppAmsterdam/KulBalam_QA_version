from sqlalchemy import create_engine, MetaData, event
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = 'sqlite:///./kulbalam.db'

engine= create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}
)

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush= False, bind=engine)

Base= declarative_base()

metadata = MetaData()
metadata.reflect(bind=engine)

def get_db(): #get a db session
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()
