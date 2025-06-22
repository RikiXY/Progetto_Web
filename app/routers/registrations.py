from typing import Annotated
from fastapi import APIRouter, HTTPException, Query
from app.data.db import SessionDep
from sqlmodel import select
from app.models.registration import Registration, RegistrationPublic

router = APIRouter(prefix="/registrations") # Prefisso per le routes delle registrazioni /registrations

# Restituisce tutte le registrazioni
@router.get("/")  # GET /
def get_all_registrations(session: SessionDep) -> list[RegistrationPublic]:
    """Restituisce tutte le registrazioni"""
    statement = select(Registration)  # Crea una query per selezionare tutte le registrazioni
    registrations = session.exec(statement).all()  # Esegue la query e recupera tutte le registrazioni
    return registrations  # Restituisce tutte le registrazioni, trasformate automaticamente in RegistrationPublic

# Cancella una registrazione specifica
@router.delete("/")  # DELETE /?username={username}&event_id={event_id}
def delete_registration(
        session: SessionDep,
        username: Annotated[str, Query(description="The username of the user to delete registration for")],  # Parametro di query per l'username
        event_id: Annotated[int, Query(description="The ID of the event to delete registration for")]  # Parametro di query per l'ID dell'evento
    ):
    """Cancella una registrazione specifica per un utente e un evento"""
    registration = session.get(Registration, (username, event_id))  # Recupera la registrazione specifica usando username e event_id come chiavi primarie
    if registration is None:
        raise HTTPException(status_code=404, detail="Registration not found")  # Se la registrazione non esiste, solleva un'eccezione HTTP 404
    session.delete(registration)  # Elimina la registrazione dal database
    session.commit()  # Applica le modifiche al database
    return "Registration successfully deleted"