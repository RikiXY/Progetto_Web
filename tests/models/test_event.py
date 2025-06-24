import pytest 
from datetime import datetime
from pydantic import ValidationError
from sqlmodel import Session
from app.models.event import Event, EventCreate

# Test per la creazione di un evento
def test_event_creation(session: Session):
    event = Event(
        title = "Hackaton",
        description = "Sfida di programmazione",
        date = datetime(2025, 6, 24, 23, 00),
        location = "Universotà degli studi di Cagliari"
    )
    session.add(event)  # Aggiunge l'evento alla sessione
    session.commit()  # Conferma le modifiche
    
    stored_event = session.get(Event, event.id)  # Recupera l'evento dal database   
    assert stored_event is not None  # Controlla che l'evento sia stato salvato 
    assert stored_event.title == "Hackaton"  # Controlla che il titolo sia corretto 
    assert stored_event.description == "Sfida di programmazione"  # Controlla che la descrizione sia corretta
    assert stored_event.date == datetime(2025, 6, 24, 23, 00)  # Controlla che la data sia corretta 
    assert stored_event.location == "Universotà degli studi di Cagliari"  # Controlla che la location sia corretta  
    
# Test per la validazione dei vincoli dell'evento   
def test_event_field_validation(session: Session):
    with pytest.raises(ValidationError):
        EventCreate(
            title = "", # Titolo troppo corto, dev'essere almeno 1 carattere      
            description = "Descrizione valida",   
            date = datetime(2025, 6, 24, 23, 00),
            location = "Location valida" 
        )
    with pytest.raises(ValidationError):
        EventCreate(
            title = "x"*101,  # Titolo troppo lungo, dev'essere al massimo 100 caratteri
            description = "Descrizione valida",   
            date = datetime(2025, 6, 24, 23, 00), 
            location = "Location valida"
        )
    with pytest.raises(ValidationError):
        EventCreate(
            title = "Titolo valido", 
            description = "Descrizione valida",
            date = datetime(2025, 6, 24, 23, 00),
            location = ""  # Location troppo corta, dev'essere almeno 1 carattere   
        )
    with pytest.raises(ValidationError):                            
        EventCreate(
            title = "Titolo valido", 
            description = "Descrizione valida",
            date = datetime(2025, 6, 24, 23, 00),
            location = "x"*101  # Location troppo lunga, dev'essere al massimo 100 caratteri
        )
            
    
    