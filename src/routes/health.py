from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.utils.db import get_db
from src.utils.redis_client import redis_client

health_router = APIRouter()


@health_router.get("/health", status_code=status.HTTP_200_OK)
def health_check(db: Session = Depends(get_db)):
    health = {
        "status": "healthy",
        "database": "healthy",
        "redis": "healthy",
    }

    try:
        db.execute(text("SELECT 1"))
    except Exception:
        health["database"] = "unhealthy"
        health["status"] = "unhealthy"

    try:
        redis_client.ping()
    except Exception:
        health["redis"] = "unhealthy"
        health["status"] = "unhealthy"

    return health