from fastapi import APIRouter
from app.data.db import SessionDep
from sqlmodel import select
from app.models.user import User, UserCreate, UserPublic

router = APIRouter(prefix="/users")

@router.get("/")
def get_all_users(session: SessionDep) -> list[UserPublic]:
    """Ritorna tutti gli utenti registrati."""
    query = select(User)  # Crea una query per selezionare tutti gli utenti
    users = session.exec(query).all()  # Esegue la query e ottiene tutti gli utenti
    return f"List of users: {users}"

@router.post("/")
def add_user(user: UserCreate, session: SessionDep) -> UserPublic:
    """Aggiunge un nuovo utente."""
    validated_user = User.model_validate(user)
    session.add(validated_user)  # Aggiunge l'utente alla sessione
    session.commit()
    return f"User {validated_user.username} added successfully."

