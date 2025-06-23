import pytest
from pydantic import ValidationError
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import User, UserCreate

# Test per la creazione di un utente
def test_user_creation(session: Session):
    user = User(username="mario_rossi", name="Mario Rossi", email="mario@rossi.com")
    session.add(user)  # Aggiunge l'utente alla sessione
    session.commit()  # Conferma le modifiche al database

    stored_user = session.get(User, "mario_rossi")  # Recupera l'utente dal database
    assert stored_user is not None  # Controlla che l'utente sia stato salvato
    assert stored_user.username == "mario_rossi"  # Controlla che lo username sia corretto
    assert stored_user.name == "Mario Rossi"  # Controlla che il nome sia corretto
    assert stored_user.email == "mario@rossi.com"  # Controlla che l'email sia corretta

# Test per la validazione della univocità della email dell'utente
def test_user_unique_email_email_constraint(session: Session):
    user_1 = User(username="luigi_verdi", name="Luigi Verdi", email="luigi@verdi.it")
    session.add(user_1)  # Aggiunge il primo utente alla sessione
    session.commit()  # Conferma le modifiche al database

    user_2 = User(username="giovanni_blu", name="Giovanni Blu", email="luigi@verdi.it") # Prova a creare un secondo utente con la stessa email
    session.add(user_2)  # Aggiunge il secondo utente alla sessione
    with pytest.raises(IntegrityError):  # Controlla che venga sollevata un'eccezione
        session.commit() # Prova a confermare le modifiche al database

# Test per la validazione dei vincoli dell'utente
def test_user_field_validation(session: Session):
    with pytest.raises(ValidationError):
        UserCreate(username="utente_invalido", name="", email="invalido@example.org")  # Nome troppo corto, dev'essere almeno 1 carattere
    with pytest.raises(ValidationError):
        UserCreate(username="utente_invalido", name="x"*51, email="invalido@example.org") # Nome troppo lungo, dev'essere al massimo 50 caratteri

    with pytest.raises(ValidationError):
        UserCreate(username="utente_invalido", name="Utente Invalido", email="")  # Email troppo corta, dev'essere almeno 1 carattere
    with pytest.raises(ValidationError):
        UserCreate(username="utente_invalido", name="Utente Invalido", email="x"*101)  # Email troppo lunga, dev'essere al massimo 100 caratteri