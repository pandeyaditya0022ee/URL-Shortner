from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.utils.db import get_db
from src.schemas.auth import UserRegisterSchema, UserResponseSchema,TokenResponseSchema,LoginSchema
from src.services import auth_service

auth_router = APIRouter(prefix="/auth")

@auth_router.post("/register",response_model=UserResponseSchema,status_code=status.HTTP_201_CREATED)
def user_registration(body : UserRegisterSchema,db:Session = Depends(get_db)):
    return auth_service.register_user(body,db)

@auth_router.post("/login",response_model=TokenResponseSchema,status_code=status.HTTP_200_OK)
def login_user(body : LoginSchema, db : Session = Depends(get_db)):
    return auth_service.login_user(body,db)