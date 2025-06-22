from sqlmodel import SQLModel, Field

class BaseUser(SQLModel):
    username: str = Field(primary_key=True)  # Imposta username come chiave primaria
    name: str = Field(min_length=1, max_length=50)  # Controlla la lunghezza del nome 
    email: str = Field(index=True, unique=True, min_length=1, max_length=100)  # Controlla la lunghezza dell'email e verifica l'unicità inserendo anche l'indice
    
# Definisce la tabella nel database
class User(BaseUser, table=True):  
    pass 

# Definisce quello che viene restituito dall'API
class UserPublic(BaseUser):  
    pass

# Definisce quello che viene richiesto nell'API per creare un nuovo utente 
class UserCreate(BaseUser):
    pass 
