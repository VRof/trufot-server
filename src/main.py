from fastapi import FastAPI

from src.api.routers.ping_router import router as ping_router
from src.api.routers.pills_router import router as pills_router
from src.api.routers.photo_router import router as photo_router
from src.db.database import Base, engine

Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(ping_router)
app.include_router(pills_router)
app.include_router(photo_router)