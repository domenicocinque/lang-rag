from sqlmodel import Session
from src.core.db import create_db, drop_db, engine  # noqa


def main() -> None:
    with Session(engine) as session:
        # drop_db()
        create_db(session)


if __name__ == "__main__":
    main()
