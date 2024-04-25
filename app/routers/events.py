from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from ..database.models import EventDB, EventDetails
from ..database.database import get_session

router = APIRouter(prefix='/events')


@router.get("/", response_model=list[EventDetails])
def get_events(session: Session = Depends(get_session), type: str = None):
    if type and type not in ["level_started", "level_solved"]:
        raise HTTPException(status_code=400)
    
    query = select(EventDB)
    if type:
        query = query.where(EventDB.type == type)
    
    events = session.exec(query).all()
    return events