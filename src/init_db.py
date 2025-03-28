from sqlmodel import Session
from src.core.db import create_db, engine   


def main():
    with Session(engine) as session:
        create_db(session)


if __name__ == "__main__":
    main()
