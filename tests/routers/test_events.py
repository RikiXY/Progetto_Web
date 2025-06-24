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
        json = {"user_id": user.username}  
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
            json={"user_id": user.username} 
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
        json = {"user_id": user.username}
    )  
    
    # Invio una richiesta POST per registrare nuovamente l'utente all'evento
    response = client.post( 
        f"/events/{event.id}/register", 
        json = {"user_id": user.username}  
    )
    
    assert response.status_code == 400  # Controlla che il codice di stato sia 400 (Bad Request)
    assert response.json()["detail"] == "User already registered for this event"  # Controlla che la risposta sia corretta
    
