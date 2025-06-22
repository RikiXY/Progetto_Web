from typing import Annotated
from fastapi import APIRouter, HTTPException, Path
from app.data.db import SessionDep
from sqlmodel import delete, select
from app.models.event import Event, EventCreate, EventPublic
from app.models.registration import Registration, RegistrationCreate
from app.models.user import User

router = APIRouter(prefix ="/events") 

@router.get("/")
def get_all_events(session: SessionDep) -> list[EventPublic]:  # SessionDep apre una sessione del database, con cui si potrà fare query, etc.
    # la funzione restituirà una lista di oggetti EventPublic
    """Restituisce tutti gli eventi"""
    statement = select(Event)  # costruisce una query, questa andrà a cercare tutti gli eventi nel DB
    events = session.exec(statement).all()  # ottiene tutti i risultati della query come lista di oggetti
    return events  # la lista viene restituita come risposta dell'API

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
    return f"Event {event.id} successfully updated"

@router.delete ("/")
def delete_all_events(session: SessionDep):  # viene definita la funzione 
    """Cancella tutti gli eventi"""
    statement = delete(Event)  # viene creata una query per cancellare tutte le righe della righe della tabella Event
    session.exec(statement)  # viene eseguita la query sul db usando la sessione attiva
    session.commit()  # conferma le modifiche fatte durante la sessione, rendendole definitive
    return "All events successfully deleted"

@router.delete("/{event_id}")  
def delete_event(
        session: SessionDep,  # Sessione del database
        event_id: Annotated[int, Path(description="The ID of the event to delete")] 
    ):  
    """ 
    Elimina un evento in base all'ID.
    """
    event = session.get(Event, event_id)  # recupera l'evento dal database usando l'ID (chiave primaria)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")  # Solleva un'eccezione HTTP 404 se l'evento non esiste  
    session.delete(event)  # cancella l'evento dal database
    session.commit()  # conferma le modifiche al database
    return f"Event {event_id} successfully deleted"

@router.post("/{event_id}/register")    
def register_for_event(
        session: SessionDep,  # Sessione del database
        event_id: Annotated[int, Path(description="The ID of the event to register for")], 
        registration: RegistrationCreate  # Dati inviati per la registrazione         
    ):  
    """ 
    Registra un utente per un evento specifico.
    """ 
    if session.get(Event, event_id) is None:  # Controlla se l'evento esiste
        raise HTTPException(status_code=404, detail="Event not found")  # Solleva un'eccezione HTTP 404 se l'evento non esiste
    if session.get(User, registration.username) is None:  # Controlla se l'utente esiste    
        raise HTTPException(status_code=404, detail="User not found")   # Solleva un'eccezione HTTP 404 se l'utente non esiste  
    if session.get(Registration, (registration.username, event_id)) is not None:  # Controlla se l'utente è già registrato per l'evento
        raise HTTPException(status_code=400, detail="User already registered for this event")  # Solleva un'eccezione HTTP 400 se l'utente è già registrato
    
    complete_registration = Registration(username=registration.username, event_id=event_id)  # Crea un oggetto Registration completo        
    validated_registration = Registration.model_validate(complete_registration)  # Valida l'oggetto Registration        
    session.add(validated_registration)  # Aggiunge la registrazione al database          
    session.commit()  # Conferma le modifiche al database
    return f"User {registration.username} successfully registered for event {event_id}" 

@router.post("/")
def add_event(event: EventCreate, session: SessionDep):  # viene aggiunto un nuovo evento
    """Aggiunge un nuovo evento"""
    validated_event = Event.model_validate(event)  # validazione e creazione dell'evento per il db
    session.add(validated_event)  # viene aggiunto il nuovo evento alla sessione
    session.commit()  # con il commit viene salvato il nuovo evento nel db
    return "Event successfully added"  

@router.get("/{event_id}")
def get_event(
        session: SessionDep,
        event_id: Annotated[int, Path(description="The ID of the event to get")]  # prende il parametro event_id 
    ) -> EventPublic:  # formato nel quale sarà serializzato
    """Restituisce un evento dato il suo ID."""
    event = session.get(Event, event_id)  # viene cercato nel db l'evento con chiave primaria uguale a event_id
    if event is None:  # se non esiste un evento con quell'ID, viene sollevata un'eccezione HTTP 404
        raise HTTPException(status_code = 404, detail ="Event not found")  # messaggio mostrato
    return event
