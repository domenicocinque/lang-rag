from sqlmodel import create_engine, SQLModel

from src.core.config import settings

engine = create_engine(settings.DATABASE_URL)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def drop_db() -> None:
    SQLModel.metadata.drop_all(engine)
