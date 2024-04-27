from fastapi import HTTPException
from .models import PlayerDB, PlayerBase, PlayerCreate
from sqlmodel import Session, select


def create_player(session: Session, player_in: PlayerCreate):
    player_db = PlayerDB.model_validate(player_in)
    session.add(player_db)
    session.commit()
    session.refresh(player_db)
    return player_db


def get_players(session: Session, name: str = ""):
    if name != "":
        return session.exec(select(PlayerDB).where(PlayerDB.name == name)).all()
    return session.exec(select(PlayerDB)).all()


def get_player(session: Session, id: int):
    player = session.get(PlayerDB, id)
    if not player:
        raise HTTPException(status_code=404)
    return player


# def delete_player(session: Session, id: int):
#     player = session.get(PlayerDB, id)
#     if not player:
#         raise HTTPException(status_code=404)
#     session.delete(player)
#     session.commit()
#     return {'message': f'player with id {id} deleted'}