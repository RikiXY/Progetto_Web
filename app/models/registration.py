from sqlmodel import SQLModel, Field

# Modello di base per la registrazione
class RegistrationBase(SQLModel):
    pass
    
# Definisce la tabella nel database
class Registration(RegistrationBase, table=True):
    # username e event_id sono le chiavi primarie (e chiavi esterne) della tabella Registration
    # Entrambi sono impostati come ondelete="CASCADE" per eliminare le registrazioni associate quando l'utente o l'evento vengono eliminati
    username: str = Field(primary_key=True, foreign_key="user.username", ondelete="CASCADE")  # Chiave primaria e chiave esterna usando l'username dell'utente
    event_id: int = Field(primary_key=True, foreign_key="event.id", ondelete="CASCADE")  # Chiave primaria e chiave esterna usando l'ID dell'evento

# Definisce quello che viene restituito dall'API
class RegistrationPublic(RegistrationBase):
    username: str
    event_id: int

# Definisce quello che viene richiesto nel body della richiesta all'API per creare una nuova registrazione
# Solo l'username è richiesto, l'event_id viene recuperato dal percorso dell'API
class RegistrationCreate(RegistrationBase):
    username: str