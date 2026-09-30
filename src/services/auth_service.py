import string, random
from sqlalchemy.orm import Session
from src.schemas.url import UrlSchema
from src.models.user import UserModel
from src.schemas.auth import UserRegisterSchema, LoginSchema
from src.utils.security import (
    get_password_hash,
    verify_password,
    create_jwt_token,
    verify_jwt_token,
)
from src.models.url import UrlModel
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from sqlalchemy.exc import IntegrityError
from jwt.exceptions import InvalidTokenError,ExpiredSignatureError




def register_user(body: UserRegisterSchema, db: Session):
    username = db.query(UserModel).filter(UserModel.username == body.username).first()
    email = db.query(UserModel).filter(UserModel.email == body.email).first()

    if username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username Already Exists..........",
        )
    if email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email Already Exists..........",
        )

    new_user = UserModel(
        username=body.username,
        email=body.email,
        hash_password=get_password_hash(body.password),
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Required Unique Constrant.............",
        )

    return new_user


def login_user(body: LoginSchema, db: Session):
    user: UserModel = (
        db.query(UserModel).filter(UserModel.username == body.username).first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are Not Authorized.........",
        )

    if not verify_password(body.password, user.hash_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are Not Authorized.........",
        )

    token = create_jwt_token(user.id, user.username)
    return {"access_token": token, "token_type": "bearer"}



    