from fastapi.testclient import TestClient
from sqlmodel import Session, select
from app.models.user import User



# Test per Users@GET("/") con dati
def test_get_all_users_with_data(client: TestClient, session: Session):
    session.add(User(username="paolo", name="Paolo Rossi", email="paolo@rossi.org"))  # Aggiungo un utente al database
    session.add(User(username="anna", name="Anna Bianchi", email="anna@bianchi.org"))  # Aggiungo un altro utente al database
    session.commit()

    response = client.get("/users/")  # Effettuo una richiesta GET per ottenere tutti gli utenti
    assert response.status_code == 200
    payload = response.json()  # Ottengo il payload della risposta
    assert len(payload) == 2  # Controllo che ci siano due utenti
    assert payload[0] == {"username": "paolo", "name": "Paolo Rossi", "email": "paolo@rossi.org"}  # Controllo il primo utente
    assert payload[1] == {"username": "anna", "name": "Anna Bianchi", "email": "anna@bianchi.org"}  # Controllo il secondo utente

# Test per Users@GET("/") se non ci sono utenti
def test_get_all_users_empty(client: TestClient):
    response = client.get("/users/")  # Effettuo una richiesta GET per ottenere tutti gli utenti
    assert response.status_code == 200
    assert response.json() == []  # Controllo che la risposta sia una lista vuota, poiché non ci sono utenti nel database



# Test per Users@POST("/") per aggiungere un utente 
def test_add_user_success(client: TestClient, session: Session):
    response = client.post("/users/", json={  # Aggiungo un utente tramite una richiesta POST
        "username": "paolo",
        "name": "Paolo Rossi",
        "email": "paolo@rossi.org"
    })
    assert response.status_code == 200  # Controllao che la risposta sia 200 OK
    assert response.json() == "User paolo added successfully."  # Controllo il messaggio di successo

    stored_user = session.get(User, "paolo")  # Recupero l'utente dal database
    assert stored_user is not None  # Controllo che l'utente sia stato salvato
    assert stored_user.username == "paolo"  # Controllo che lo username sia corretto
    assert stored_user.name == "Paolo Rossi"  # Controllo che il nome sia corretto
    assert stored_user.email == "paolo@rossi.org"  # Controllo che l'email sia corretta



# Test per Users@DELETE("/") per cancellare tutti gli utenti
def test_delete_all_users(client: TestClient, session: Session):
    session.add(User(username="paolo", name="Paolo Rossi", email="paolo@rossi.org"))  # Aggiungo un utente al database
    session.add(User(username="anna", name="Anna Bianchi", email="anna@bianchi.org"))  # Aggiungo un altro utente al database
    session.commit()

    resp = client.delete("/users/")  # Eseguo una DELETE per cancellare tutti gli utenti
    assert resp.status_code == 200  # Controllo che la risposta sia 200 OK
    assert resp.json() == "All users successfully deleted"  # Controllo il messaggio di successo

    assert len(session.exec(select(User)).all()) == 0  # Verifico che non ci siano più utenti nel database



# Test per Users@GET("/{username}") per recuperare un utente
def test_get_user_by_username_success(client: TestClient, session: Session):
    session.add(User(username="anna", name="Anna Bianchi", email="anna@bianchi.org"))  # Aggiungo un utente al database
    session.commit()

    resp = client.get("/users/anna")  # Recupero l'utente tramite una richiesta GET
    assert resp.status_code == 200  # Controlla che la risposta sia 200 OK
    data = resp.json()
    assert data["username"] == "anna"  # Controlla che lo username sia corretto
    assert data["name"] == "Anna Bianchi"  # Controlla che il nome sia corretto
    assert data["email"] == "anna@bianchi.org"  # Controlla che l'email sia corretta

# Test per Users@GET("/{username}") per recuperare un utente che non esiste
def test_get_user_not_found(client: TestClient):
    response = client.get("/users/inesistente")  # Provo a recuperare un utente che non esiste
    assert response.status_code == 404  # Controllo che la risposta sia 404 Not Found
    assert response.json()["detail"] == "User not found"  # Controllo il messaggio di errore