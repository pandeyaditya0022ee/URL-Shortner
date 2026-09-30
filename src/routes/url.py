
from fastapi import APIRouter, Depends,status
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from src.utils.db import get_db
from src.schemas.url import UrlSchema,UrlResponseSchema
from src.services import url_service
from typing import List

url_router = APIRouter(prefix="/url")


@url_router.post("/urls",response_model=UrlResponseSchema,status_code=status.HTTP_201_CREATED)
def create_url(body : UrlSchema,db : Session = Depends(get_db)):
    return url_service.create_url(body,db)
    

@url_router.get("/redirect/{short_code}",status_code=status.HTTP_200_OK)
def redirect_url(short_code : str,db : Session = Depends(get_db)):
    url = url_service.redirect_url(short_code,db)
    
    return RedirectResponse(url=url)
    
    
@url_router.get("/detail/{url_id}",response_model=UrlResponseSchema,status_code=status.HTTP_200_OK)
def get_url_detail(url_id : int, db : Session = Depends(get_db)):
    return url_service.get_url_detail(url_id,db)

@url_router.get("/all",response_model=List[UrlResponseSchema],status_code=status.HTTP_200_OK)
def get_all_url(db:Session = Depends(get_db)):
    return url_service.get_all_url(db)

@url_router.patch("/deactivate/{url_id}",status_code=status.HTTP_200_OK,response_model=UrlResponseSchema)
def deactivate_url(url_id : int,db : Session = Depends(get_db)):
    return url_service.deactivate_url(url_id,db)