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
    """Returns all events"""
    statement = select(Event)  # costruisce una query, questa andrà a cercare tutti gli eventi nel DB
    events = session.exec(statement).all()  # ottiene tutti i risultati della query come lista di oggetti
    return events  # la lista viene restituita come risposta dell'API



