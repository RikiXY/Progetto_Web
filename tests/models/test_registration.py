import pytest
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from app.models.user import User
from app.models.event import Event
from app.models.registration import Registration

# Creazione di un utente e di un evento per i test
def create_user_event(session: Session):
    user = User(username="paolo", name="Paolo Rossi", email="paolo@rossi.com")
    event = Event(title="Evento non generico", description="Monthly meetup", date=datetime(2025, 6, 18, 14, 30), location="Luogo non generico")
    session.add(user)
    session.add(event)
    session.commit()
    return user, event

# Test per la creazione di una registrazione
def test_registration_creation(session: Session):
    user, event = create_user_event(session)

    registration = Registration(username=user.username, event_id=event.id)
    session.add(registration)
    session.commit()

    stored_registration = session.get(Registration, (user.username, event.id))
    assert stored_registration is not None
    assert stored_registration.username == user.username
    assert stored_registration.event_id == event.id

# Test per la validazione della univocità della registrazione
def test_registration_composite_pk_constraint(session: Session):
    user, event = create_user_event(session)

    registration_1 = Registration(username=user.username, event_id=event.id)
    session.add(registration_1)
    session.commit()
    session.expunge(registration_1)

    registration_2 = Registration(username=user.username, event_id=event.id)
    session.add(registration_2)
    with pytest.raises(IntegrityError):
        session.commit()

# Test per la validazione delle eliminazioni a cascata sull'utente
def test_registration_cascade_on_user_delete(session: Session):
    user, event = create_user_event(session)
    session.add(Registration(username=user.username, event_id=event.id))
    session.commit()

    # Cancellare l'utente dovrebbe cancellare la registrazione a cascata
    session.delete(user)
    session.commit()

    assert session.get(Registration, (user.username, event.id)) is None

# Test per la validazione delle eliminazioni a cascata sull'evento
def test_registration_cascade_on_event_delete(session: Session):
    user, event = create_user_event(session)
    session.add(Registration(username=user.username, event_id=event.id))
    session.commit()

    # Cancellare l'evento dovrebbe cancellare la registrazione a cascata
    session.delete(event)
    session.commit()

    assert session.get(Registration, (user.username, event.id)) is None
