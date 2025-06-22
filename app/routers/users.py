from typing import Annotated    
from fastapi import APIRouter, HTTPException, Path
from app.data.db import SessionDep 
from sqlmodel import select, delete
from app.models.user import User, UserCreate, UserPublic

router = APIRouter(prefix="/users")

@router.get("/")
def get_all_users(session: SessionDep) -> list[UserPublic]:
    """Ritorna tutti gli utenti registrati."""
    query = select(User)  # Crea una query per selezionare tutti gli utenti
    users = session.exec(query).all()  # Esegue la query e ottiene tutti gli utenti
    return users

@router.post("/")
def add_user(user: UserCreate, session: SessionDep):
    """Aggiunge un nuovo utente."""
    validated_user = User.model_validate(user)
    session.add(validated_user)  # Aggiunge l'utente alla sessione
    session.commit()
    return f"User {validated_user.username} added successfully."

@router.delete("/")
def delete_all_users(session: SessionDep):
    """Cancella tutti gli utenti."""
    query = delete(User)  # Crea una query per cancellare tutti gli utenti
    session.exec(query)
    session.commit() 
    return "All users successfully deleted"

@router.get("/{username}")
def get_user(
        session: SessionDep,
        username: Annotated[str, Path(description="The username of the user to retrieve")]
    ) -> UserPublic:
    """Restituisce un utente specifico secondo l'username."""
    user = session.get(User, username)
    if user is None: 
        raise HTTPException(status_code=404, detail="User not found")  # Solleva un'eccezione HTTP 404 se l'utente non esiste
    return user

@router.delete("/{username}")
def delete_user(
    session: SessionDep,  # Sessione del database
    username: Annotated[str, Path(description="The username of the user to delete")] 
    ):
    """
    Elimina un utente in base al nome utente.
    """
    user = session.get(User, username)  # recupero l'utente dal db usando l'username (chiave primaria)
    if user is None: 
        raise HTTPException(status_code=404, detail="User not found")  # Sollevo un'eccezione  HTTP 404 se l'utente non esiste 
    session.delete(user)  # cancella l'utente dal database
    session.commit()  # conferma le modifiche al database   
    return f"User {username} deleted successfully."