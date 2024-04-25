from contextlib import asynccontextmanager
from fastapi import FastAPI
from .routers import players, events
from .database.database import create_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("startataan")
    # luo tietokanta
    create_db()
    yield
    print("lopetellaan")

app = FastAPI(lifespan=lifespan)


app.include_router(players.router)
app.include_router(events.router)