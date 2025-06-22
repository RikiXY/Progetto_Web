from typing import Annotated    
from fastapi import APIRouter, HTTPException, Path
from app.data.db import SessionDep 
from app.models.user import User, UserCreate, UserPublic

router = APIRouter(prefix="/users")

@router.delete("/{username}")
def delete_user(
    session: SessionDep,  # Sessione del database
    username: Annotated[str, Path(description="The username of the user to delete")] 
    ):
    """
    Delete a user by username.
    """
    user = session.get(User, username)  # recupero l'utente dal db usando l'username (chiave primaria)
    if user is None: 
        raise HTTPException(status_code=404, detail="User not found")  # Sollevo un'eccezione  HTTP 404 se l'utente non esiste 
    session.delete(user) # cancella l'utente dal database
    session.commit() # conferma le modifiche al database   
    return "User successfully deleted"

