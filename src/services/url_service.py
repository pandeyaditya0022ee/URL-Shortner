import string, random
from sqlalchemy.orm import Session
from src.schemas.url import UrlSchema
from src.models.url import UrlModel
from src.models.user import UserModel
from src.models.click import ClickModel
from src.utils.redis_client import redis_client
from fastapi import HTTPException, status, Query
from datetime import datetime
from sqlalchemy.exc import IntegrityError
import json
from src.utils.logger import logger


def get_short_code(db: Session):
    characters = string.ascii_letters + string.digits
    while True:
        code = ""
        for i in range(6):
            code += random.choice(characters)
        if is_code_available(code, db):
            return code


def is_code_available(code: str, db: Session):
    exist = db.query(UrlModel).filter(UrlModel.short_code == code).first()

    if not exist:
        return True

    return False


def create_url(body: UrlSchema, db: Session, user: UserModel):
    # data = body.model_dump()

    new_data = UrlModel(
        original_url=body.original_url,
        # original_url = data["original_url"],
        short_code=get_short_code(db),
        expires_at=body.expires_at,
        user_id=user.id,
    )
    try:
        db.add(new_data)
        db.commit()
        db.refresh(new_data)
        logger.info(
            "URL created | user_id=%s | url_id=%s | short_code=%s",
            user.id,
            new_data.id,
            new_data.short_code,
        )

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Required Unique Constrant...........",
        )

    return new_data


def redirect_url(short_code: str, db: Session):
    key = f"url:{short_code}"
    raw_data = redis_client.get(key)

    if raw_data:
        logger.info("Cache HIT | short_code=%s", short_code)
        cached_url = json.loads(raw_data)

        if cached_url["is_active"] is False:
            logger.warning(
                "Inactive URL accessed | short_code=%s",
                short_code,
            )
            raise HTTPException(
                status_code=status.HTTP_410_GONE,
                detail="Url is No Longer Active.........",
            )
        if cached_url["expires_at"] is not None:
            expire = datetime.fromisoformat(cached_url["expires_at"])
            if expire < datetime.now():
                raise HTTPException(
                    status_code=status.HTTP_410_GONE, detail="Url is expired......"
                )

    else:
        logger.info("Cache MISS | short_code=%s", short_code)
        data: UrlModel = (
            db.query(UrlModel).filter(UrlModel.short_code == short_code).first()
        )

        if not data:
            logger.warning(
                "URL not found | short_code=%s",
                short_code,
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Url Not Found........."
            )

        if data.is_active is False:
            raise HTTPException(
                status_code=status.HTTP_410_GONE,
                detail="Url is No Longer Active.........",
            )

        if data.expires_at is not None and data.expires_at < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_410_GONE, detail="Url is expired......"
            )

        cached_url = {
            "id": data.id,
            "original_url": data.original_url,
            "is_active": data.is_active,
            "expires_at": data.expires_at.isoformat() if data.expires_at else None,
        }
        redis_client.set(
            key,
            json.dumps(cached_url),
            ex=60 * 5,
        )  # remain in cache for 5 min

    click_data = ClickModel(url_id=cached_url["id"])

    try:
        db.add(click_data)
        db.commit()
        db.refresh(click_data)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Required Unique Constrant...........",
        )
    logger.info(
        "URL redirected | short_code=%s | url_id=%s",
        short_code,
        cached_url["id"],
    )
    return cached_url["original_url"]


def get_url_detail(url_id: int, db: Session, user: UserModel):
    url: UrlModel = db.query(UrlModel).filter(UrlModel.id == url_id).first()

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    if url.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this URL")

    return url




def deactivate_url(url_id: int, db: Session, user: UserModel):
    url: UrlModel = db.query(UrlModel).filter(UrlModel.id == url_id).first()

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    if url.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this URL")

    url.is_active = False

    db.commit()
    db.refresh(url)

    return url


def get_my_urls(page: int, limit: int, user: UserModel, db: Session):
    query = db.query(UrlModel).filter(UrlModel.user_id == user.id)

    query = query.order_by(UrlModel.created_at.desc())

    offset = (page - 1) * limit

    urls = query.offset(offset).limit(limit).all()

    return urls


def get_analytics(url_id: int, db: Session, user: UserModel):

    url: UrlModel = db.query(UrlModel).filter(UrlModel.id == url_id).first()

    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="URL not found"
        )
    if url.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    count = db.query(ClickModel).filter(ClickModel.url_id == url_id).count()

    return {"url_id": url_id, "total_clicks": count}
