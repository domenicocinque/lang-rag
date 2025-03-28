from sqlmodel import create_engine, SQLModel, text, Session

from src.core.config import settings
from src.models import TranslationPair # noqa

engine = create_engine(settings.DATABASE_URL, echo=True)


def create_db(session: Session) -> None:
    with session.begin():
        session.exec(text("CREATE EXTENSION IF NOT EXISTS vector"))

    SQLModel.metadata.create_all(engine)


def drop_db() -> None:
    SQLModel.metadata.drop_all(engine)
