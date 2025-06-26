from fastapi.testclient import TestClient
from sqlmodel import Session, select
from datetime import datetime
from app.models.event import Event
from app.models.user import User
from app.models.registration import Registration

#Creazione di un utente e di un evento per i test
def create_test_user_event(session: Session):
    user = User(
            username = "Naska",
            name = "Diego Caterbetti",  
            email = "diego.caterbetti@gmail.com",   
    )
    event = Event(
            title = "Slam Dunk",
            description = "Festival musica rock",   
            date = datetime(2025, 6, 2, 21, 0),
            location = "Carroponte",
    )
    session.add(user)  #Aggiungi l'utente al database   
    session.add(event)  #Aggiungi l'evento al database  
    session.commit()  #Salva le modifiche 
    return user, event


# Test per eliminare un evento con successo
def test_delete_event_success(client: TestClient, session: Session):    
    event = create_test_user_event(session)[1]  #  Creo un evento di test
    response = client.delete(f"/events/{event.id}")  # Invio una richiesta DELETE per eliminare l'evento con ID 1
    
    assert response.status_code ==  200  # Controlla che il codice di stato sia 200 (OK)
    assert response.json() == f"Event {event.id} successfully deleted"  # Controlla che la risposta sia corretta
    assert session.get(Event, event.id) is None  # Controlla che l'evento sia stato eliminato
    
# Test per eliminare un evento che non esiste
def test_delete_event_not_found(client: TestClient):
    response = client.delete(f"/events/999")  # Invio una richiesta DELETE per eliminare l'evento con ID 999 che non esiste

    assert response.status_code == 404  # Controlla che il codice di stato sia 404 (Not Found)
    assert response.json()["detail"] == "Event not found"  # Controlla che la risposta sia corretta   
    
# Test per registrare un untente a un evento con successo
def test_register_event_success(client: TestClient, session: Session):
    user, event = create_test_user_event(session)  # Creo un utente e un evento di test
    response = client.post(
        f"/events/{event.id}/register", 
        json = {"username": user.username}  
    )  # Invio una richiesta POST per registrare l'utente all'evento
    
    registration = session.get(Registration, (user.username, event.id))  # Recupera la registrazione dal database               

    assert response.status_code == 200  # Controlla che il codice di stato sia 200 (OK)
    assert response.json() == f"User {user.username} successfully registered for event {event.id}"  # Controlla che la risposta sia corretta    
    assert registration is not None  # Controlla che la registrazione sia stata creata  
    
# Test per registrare un utente a un evento che non esiste  
def test_register_event_not_found(client: TestClient, session: Session):
    user = create_test_user_event(session)[0]  # Creo un utente di test
    response = client.post(
            f"/events/999/register", 
            json={"username": user.username} 
    )  # Invio una richiesta POST per registrare l'utente all'evento con ID 999 che non esiste
    
    assert response.status_code == 404  # Controlla che il codice di stato sia 404 (Not Found)  
    assert response.json()["detail"] == "Event not found"  # Controlla che la risposta sia corretta
    
# Test per registrare un utente a un evento con un utente che non esiste    
def test_register_event_user_not_found(client: TestClient, session: Session):
    event = create_test_user_event(session)[1]  # Creo un evento di test
    response = client.post(
        f"/events/{event.id}/register", 
        json = {"username": "Inesistente"}  
    )  # Invio una richiesta POST per registrare un utente che non esiste all'evento
    
    assert response.status_code == 404  # Controlla che il codice di stato sia 404 (Not Found)
    assert response.json()["detail"] == "User not found"  # Controlla che la risposta sia corretta
    
# Test per registrare un utente a un evento a cui è già registrato
def test_register_event_already_registered(client: TestClient, session: Session):
    user, event = create_test_user_event(session)  # Creo un utente e un evento di test
    
    # Creo una registrazione per l'utente all'evento
    client.post(
        f"/events/{event.id}/register",
        json = {"username": user.username}
    )  
    
    # Invio una richiesta POST per registrare nuovamente l'utente all'evento
    response = client.post( 
        f"/events/{event.id}/register", 
        json = {"username": user.username}  
    )
    
    assert response.status_code == 400  # Controlla che il codice di stato sia 400 (Bad Request)
    assert response.json()["detail"] == "User already registered for this event"  # Controlla che la risposta sia corretta
    
# Test per recuperare gli eventi quando non ce ne sono
def test_get_all_events_empty(client: TestClient):
    response = client.get("/events/")
    assert response.status_code == 200
    assert response.json() == []

# Test per recuperare tutti gli eventi
def test_get_all_events_with_data(client: TestClient, session: Session):
    session.add(Event(title="Evento 1", description="Descrizione 1", date=datetime(2025, 6, 18, 14, 30), location="Luogo 1"))
    session.add(Event(title="Evento 2", description="Descrizione 2", date=datetime(2025, 6, 19, 14, 30), location="Luogo 2"))
    session.commit()

    response = client.get("/events/")
    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 2
    assert payload[0] == {"id": 1, "title": "Evento 1", "description": "Descrizione 1", "date": "2025-06-18T14:30:00", "location": "Luogo 1"}
    assert payload[1] == {"id": 2, "title": "Evento 2", "description": "Descrizione 2", "date": "2025-06-19T14:30:00", "location": "Luogo 2"}

# Test per aggiungere un evento con successo
def test_add_event_success(client: TestClient, session: Session):
    response = client.post("/events/", json={
        "title": "Nuovo evento",
        "description": "Descrizione del nuovo evento",
        "date": "2025-06-20T14:30:00",
        "location": "Luogo del nuovo evento"
    })
    assert response.status_code == 200
    assert response.json() == "Event successfully added"

    stored_event = session.get(Event, 1)
    assert stored_event is not None
    assert stored_event.title == "Nuovo evento"
    assert stored_event.description == "Descrizione del nuovo evento"
    assert stored_event.date == datetime(2025, 6, 20, 14, 30)
    assert stored_event.location == "Luogo del nuovo evento"

# Test per recuperare un evento con successo
def test_get_event_success(client: TestClient, session: Session):
    session.add(Event(title="Evento non generico", description="Descrizione non generica", date=datetime(2025, 6, 18, 14, 30), location="Luogo non generico"))
    session.commit()

    response = client.get(f"/events/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Evento non generico"
    assert data["description"] == "Descrizione non generica"
    assert data["date"] == "2025-06-18T14:30:00"
    assert data["location"] == "Luogo non generico"

# Test per recuperare un evento che non esiste
def test_get_event_not_found(client: TestClient):
    response = client.get("/events/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"

# Test per eliminare tutti gli eventi
def test_delete_all_events(client: TestClient, session: Session):
    session.add(Event(title="Evento 1", description="Descrizione 1", date=datetime(2025, 6, 18, 14, 30), location="Luogo 1"))
    session.add(Event(title="Evento 2", description="Descrizione 2", date=datetime(2025, 6, 19, 14, 30), location="Luogo 2"))
    session.commit()

    response = client.delete("/events/")
    assert response.status_code == 200
    assert response.json() == "All events successfully deleted"

    assert len(session.exec(select(Event)).all()) == 0