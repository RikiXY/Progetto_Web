from typing import Annotated
from fastapi import APIRouter, HTTPException, Path
from app.data.db import SessionDep
from app.models.event import Event, EventCreate

router = APIRouter(prefix="/events")

# Modifica un evento
@router.put("/{event_id}")  # PUT /{event_id}
def update_event(
        event_id: Annotated[int, Path(description="The ID of the event to update")],  # Parametro di path per l'ID dell'evento
        event_update: EventCreate,  # Body della richiesta per aggiornare l'evento
        session: SessionDep
    ):
    """Modifica un evento in base all'ID"""
    event = session.get(Event, event_id)  # Recupera l'evento specifico usando l'ID
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")  # Se l'evento non esiste, solleva un'eccezione HTTP 404
    event.title = event_update.title  # Aggiorna il titolo dell'evento
    event.description = event_update.description  # Aggiorna la descrizione dell'evento
    event.date = event_update.date  # Aggiorna la data dell'evento
    event.location = event_update.location  # Aggiorna la posizione dell'evento
    session.add(event)  # Aggiunge l'evento aggiornato alla sessione
    session.commit()  # Applica le modifiche al database
    return "Event successfully updated"