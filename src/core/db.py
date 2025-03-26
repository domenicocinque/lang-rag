from sqlmodel import create_engine, SQLModel

engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@localhost:5432/translation_db"
)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def drop_db() -> None:
    SQLModel.metadata.drop_all(engine)
