from datetime import datetime
from sqlmodel import SQLModel, Field

class BaseEvent(SQLModel):
    title: str = Field(min_length=1, max_length=50)  # vincoli sulla lunghezza della stringa
    description: str  # nessun vincolo di lunghezza
    date: datetime
    location: str = Field(min_length=1, max_length=100) # vincoli sulla lunghezza della stringa

class Event(BaseEvent, table = True):
    __table_args__ = {'sqlite_autoincrement': True}  # Abilita l'auto-incremento per SQLite
    # Anche senza sqlite_autoincrement, gli id invece di essere incrementati dall'id più grande assegnato,
    # vengono assegnati in ordine crescente, prendendone il più piccolo disponibile.
    # Per esempio se esistono eventi con id 1 e 3, creandone uno nuovo con sqlite_autoincrement avrebbe valore 4, altrimenti 2
    id: int | None = Field(default=None, primary_key=True) # dato che l'id può assumere valore None, lo specifichiamo in fase di dichiarazione 

class EventPublic(BaseEvent):
    id: int  

class EventCreate(BaseEvent):
    pass