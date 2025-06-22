from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy import event
from typing import Annotated
from fastapi import Depends
import os
from faker import Faker
from app.config import config
# TODO: remember to import all the DB models here
from app.models.registration import Registration  # NOQA
from app.models.event import Event  # NOQA
from app.models.user import User  # NOQA


sqlite_file_name = config.root_dir / "data/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args, echo=True)

# Abilita il controllo del vincolo di integrità referenziale per le chiavi esterne
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

def init_database() -> None:
    ds_exists = os.path.isfile(sqlite_file_name)
    SQLModel.metadata.create_all(engine)
    if not ds_exists:
        f = Faker("it_IT")
        with Session(engine) as session:
            for _ in range(10):
                user = User(
                    username=f.user_name(),
                    name=f.name()[:50],
                    email=f.email()[:100],
                )
                session.add(user)
            for _ in range(10):
                event = Event(
                    title=f.sentence()[:50],
                    description=f.text(),
                    date=f.date_time_this_year(),
                    location=f.city()[:100],
                )
                session.add(event)
            session.commit()


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
