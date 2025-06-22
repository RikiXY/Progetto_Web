from datetime import datetime
from sqlmodel import SQLModel, Field

class BaseEvent(SQLModel):
    title: str = Field(min_length=1, max_length=50)  # vincoli sulla lunghezza della stringa
    description: str  # nessun vincolo di lunghezza
    date: datetime
    location: str = Field(min_length=1, max_length=100) # vincoli sulla lunghezza della stringa

class Event(BaseEvent, table = True):
    id: int | None = Field(default=None, primary_key=True) # dato che l'id può assumere valore None, lo specifichiamo in fase di dichiarazione 

class EventPublic(BaseEvent):
    id: int  

class EventCreate(BaseEvent):
    pass