from datetime import datetime
from sqlmodel import SQLModel, Field

class BaseEvent(SQLModel):
    title: str = Field(min_length=1, max_length=50)
    description: str 
    date: datetime
    location: str = Field(min_length=1, max_length=100)

class Event(BaseEvent, table = True):
    id: int | None = Field(default=None, primary_key=True)

class EventPublic(BaseEvent):
    id: int  

class EventCreate(BaseEvent):
    pass