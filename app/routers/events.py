from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from ..database.models import EventDB
from ..database import events_crud
from ..database.database import get_session

router = APIRouter(prefix='/events')


@router.get("/", response_model=list[EventDB])
def get_events(type: str = None, session: Session = Depends(get_session)):
    if type not in ["level_started", "level_solved"]:
        raise HTTPException(status_code=400)
    
    query = select(EventDB).where(EventDB.type == type)
    events = session.exec(query).all()
    if not events:
        return []
    return events