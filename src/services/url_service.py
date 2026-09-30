import string, random
from sqlalchemy.orm import Session
from src.schemas.url import UrlSchema
from src.models.url import UrlModel
from src.models.user import UserModel
from src.models.click import ClickModel
from fastapi import HTTPException, status, Query
from datetime import datetime
from sqlalchemy.exc import IntegrityError


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

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Required Unique Constrant...........",
        )

    return new_data


def redirect_url(short_code: str, db: Session, user: UserModel):
    data: UrlModel = (
        db.query(UrlModel).filter(UrlModel.short_code == short_code).first()
    )

    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Url Not Found........."
        )

    if data.is_active is False:
        raise HTTPException(
            status_code=status.HTTP_410_GONE, detail="Url is No Longer Active........."
        )

    if data.expires_at is not None and data.expires_at < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_410_GONE, detail="Url is expired......"
        )

    click_data = ClickModel(url_id=data.id)

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

    return data.original_url


def get_url_detail(url_id: int, db: Session, user: UserModel):
    data: UserModel = db.query(UrlModel).filter(UrlModel.id == url_id).first()

    if data.id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized"
        )
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="url not found............."
        )

    return data


def get_all_url(db: Session, user: UserModel):
    data = db.query(UrlModel).all()

    return data


def deactivate_url(url_id: int, db: Session, user: UserModel):
    data: UrlModel = db.query(UrlModel).filter(UrlModel.id == url_id).first()
    if data.id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized"
        )
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Url Not Found..................",
        )

    data.is_active = False

    db.commit()
    db.refresh(data)

    return data


def get_my_urls(page: int, limit: int, user: UserModel, db: Session):
    query = db.query(UrlModel).filter(UrlModel.user_id == user.id)

    query = query.order_by(UrlModel.created_at.desc())

    offset = (page - 1) * limit

    urls = query.offset(offset).limit(limit).all()

    return urls


def get_analytics(url_id: int, db: Session, user: UserModel):
    url = (
        db.query(UrlModel)
        .filter(UrlModel.id == url_id, UrlModel.user_id == user.id)
        .first()
    )
    if not url:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="URL not found"
    )
    count = db.query(ClickModel).filter(ClickModel.url_id == url_id).count()

    return {"url_id" : url_id,"total_clicks" : count}
