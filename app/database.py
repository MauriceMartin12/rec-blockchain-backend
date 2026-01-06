from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

# echo=True pour debug SQL
engine = create_engine(settings.DATABASE_URL, echo=True, pool_pre_ping=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_db():
    with Session(engine) as session:
        yield session
