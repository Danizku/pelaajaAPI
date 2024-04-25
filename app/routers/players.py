from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel import Session
from datetime import datetime
from ..database.models import PlayerBase, PlayerDB, PlayerCreate, EventBase, EventDB
from ..database import players_crud, events_crud
from ..database.database import get_session

router = APIRouter(prefix='/players')


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PlayerDB)
def create_player(*, session: Session = Depends(get_session), player_in: PlayerCreate):
    try:
        player = players_crud.create_player(session, player_in)
    except ValueError:
        raise HTTPException(status_code=422)
    return {"id": player.id, "name": player.name}


@router.get("/", response_model=list[PlayerDB])
def get_players(session: Session = Depends(get_session)):
    return players_crud.get_players(session)


@router.get("/{id}", response_model=PlayerDB)
def get_player(*, session: Session = Depends(get_session), id: int):
    return players_crud.get_player(session, id)


@router.post("/{id}/events", status_code=status.HTTP_201_CREATED, response_model=EventDB)
def create_player_event(
    id: int, event_data: EventBase, session: Session = Depends(get_session)
):
    # tarkista onko pelaaja olemassa
    player = players_crud.get_player(session, id)
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    # tarkista eventtityyppi
    if event_data.type not in ["level_started", "level_solved"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
    # luo eventti pelaajalle
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        event = EventDB(type=event_data.type, detail=event_data.detail, timestamp=timestamp, player_id=id)
        session.add(event)
        session.commit()
        session.refresh(event)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    return event

@router.delete("/{id}")
def delete_player(*, session: Session = Depends(get_session), id: int):
    return players_crud.delete_player(session, id)