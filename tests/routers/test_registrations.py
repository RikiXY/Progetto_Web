from fastapi.testclient import TestClient
from sqlmodel import Session
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

# Test per recuperare le registrazioni quando non ce ne sono
def test_get_all_registrations_empty(client: TestClient):
    response = client.get("/registrations/")
    assert response.status_code == 200
    assert response.json() == []

# Test per recuperare tutte le registrazioni
def test_get_all_registrations_with_data(client: TestClient, session: Session):
    user, event = create_user_event(session)
    session.add(Registration(username=user.username, event_id=event.id))
    session.commit()

    response = client.get("/registrations/")
    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert payload[0] == {"username": user.username, "event_id": event.id}

# Test per eliminare una registrazione
def test_delete_registration_success(client: TestClient, session: Session):
    user, event = create_user_event(session)
    session.add(Registration(username=user.username, event_id=event.id))
    session.commit()

    delete_response = client.delete(
        "/registrations/",
        params={"username": user.username, "event_id": event.id},
    )
    assert delete_response.status_code == 200
    assert delete_response.json() == "Registration successfully deleted"

    get_response = client.get("/registrations/")
    assert get_response.status_code == 200
    assert get_response.json() == []

# Test per eliminare una registrazione che non esiste
def test_delete_registration_not_found(client: TestClient):
    response = client.delete(
        "/registrations/",
        params={"username": "ghost", "event_id": 9999},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Registration not found"