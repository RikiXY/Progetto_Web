import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, StaticPool, create_engine
from sqlalchemy import event
from app.main import app
from app.data.db import get_session
from app.models.user import User
from app.models.event import Event
from app.models.registration import Registration

# Crea una database in memoria per eseguire i test in un ambiente isolato
@pytest.fixture
def engine():
    test_engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool) # Database
    
    # Attiva il controllo dei vincoli di integrità referenziale per le chiavi esterne
    @event.listens_for(test_engine, "connect")
    def _fk_pragma(dbapi_connection, _):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    SQLModel.metadata.create_all(test_engine) # Crea le tabelle nel database di test
    try:
        yield test_engine
    finally:
        test_engine.dispose() # Chiude la connessione al database di test

# Resittuisce una sessione di test per interagire con il database
@pytest.fixture
def session(engine):
    with Session(engine) as session:
        yield session

# Restituisce un client di test per interagire con l'app FastAPI
@pytest.fixture
def client(session):
    # Sovrascrive la funzione get_session usata da FastAPI per utilizzare il database di test
    def override_get_session():
        return session

    # Sovrascrive la dipendenza get_session nell'app FastAPI
    # La dipendenza iniziale viene creata in app/data/db.py con Depends(get_session)
    app.dependency_overrides[get_session] = override_get_session
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.pop(get_session, None)
