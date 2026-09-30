from fastapi import FastAPI
from src.utils.db import Base, engine
from src.models.url import UrlModel
from src.routes.url import url_router
from src.routes.auth import auth_router
Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(url_router)
app.include_router(auth_router)