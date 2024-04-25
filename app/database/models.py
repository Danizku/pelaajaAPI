from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship


class PlayerBase(SQLModel):
    name: str


class PlayerDB(PlayerBase, table=True):
    id: int = Field(default=None, primary_key=True)
    events: list["EventDB"] = Relationship(back_populates="player")


class PlayerCreate(PlayerBase):
    pass


class EventBase(SQLModel):
    type: str
    detail: str


class EventDB(EventBase, table=True):
    id: int = Field(default=None, primary_key=True)
    timestamp: str
    player_id: int = Field(foreign_key="playerdb.id")
    player: "PlayerDB" = Relationship(back_populates="events")


class EventDetails(BaseModel):
    id: int
    type: str
    detail: str
    timestamp: str
    player_id: int

class PlayerDetails(BaseModel):
    id: int
    name: str
    events: list[EventDetails]