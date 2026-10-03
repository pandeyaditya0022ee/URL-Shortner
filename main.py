from fastapi import FastAPI
from src.utils.db import Base, engine
from src.models.url import UrlModel
from src.routes.url import url_router
from src.routes.auth import auth_router
from src.routes.health import health_router
from src.utils.exceptions import (
    AppException,
    app_exception_handler,
    unexpected_exception_handler,
)

from fastapi.middleware.cors import CORSMiddleware
from src.utils.settings import settings
from starlette.middleware.trustedhost import TrustedHostMiddleware
from src.utils.security_headers import SecurityHeadersMiddleware


app = FastAPI()
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS.split(","),
)

app.add_middleware(SecurityHeadersMiddleware)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(url_router)
app.include_router(auth_router)
app.include_router(health_router)

app.add_exception_handler(
    AppException,
    app_exception_handler,
)

app.add_exception_handler(
    Exception,
    unexpected_exception_handler,
)



