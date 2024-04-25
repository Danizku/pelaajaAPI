from fastapi import HTTPException
from .models import EventDB
from sqlmodel import Session, select

def get_events(session: Session):
    return session.exec(select(EventDB)).all()