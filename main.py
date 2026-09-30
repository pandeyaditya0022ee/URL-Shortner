from fastapi import FastAPI
from src.utils.db import Base, engine
from src.models.url import UrlModel
from src.routes.url import url_router
Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(url_router)