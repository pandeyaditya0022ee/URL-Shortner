
from fastapi import APIRouter, Depends,status,Query
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from src.utils.db import get_db
from src.schemas.url import UrlSchema,UrlResponseSchema,UrlAnalyticsSchema
from src.models.user import UserModel

from src.services import url_service
from typing import List
from src.utils.dependencies import is_authenticated
url_router = APIRouter(prefix="/url")


@url_router.post("/urls",response_model=UrlResponseSchema,status_code=status.HTTP_201_CREATED)
def create_url(body : UrlSchema,db : Session = Depends(get_db),user: UserModel = Depends(is_authenticated)):
    return url_service.create_url(body,db,user)
    

@url_router.get("/redirect/{short_code}",status_code=status.HTTP_200_OK)
def redirect_url(short_code : str,db : Session = Depends(get_db),user: UserModel = Depends(is_authenticated)):
    url = url_service.redirect_url(short_code,db,user)
    
    return RedirectResponse(url=url)
    
    
@url_router.get("/detail/{url_id}",response_model=UrlResponseSchema,status_code=status.HTTP_200_OK)
def get_url_detail(url_id : int, db : Session = Depends(get_db),user: UserModel = Depends(is_authenticated)):
    return url_service.get_url_detail(url_id,db,user)

@url_router.get("/all",response_model=List[UrlResponseSchema],status_code=status.HTTP_200_OK)
def get_all_url(db:Session = Depends(get_db),user: UserModel = Depends(is_authenticated)):
    return url_service.get_all_url(db,user)

@url_router.patch("/deactivate/{url_id}",status_code=status.HTTP_200_OK,response_model=UrlResponseSchema)
def deactivate_url(url_id : int,db : Session = Depends(get_db),user: UserModel = Depends(is_authenticated)):
    return url_service.deactivate_url(url_id,db,user)


@url_router.get("/my-urls",response_model=List[UrlResponseSchema],status_code=status.HTTP_200_OK)
def my_url(page:int = Query(1,ge=1),limit:int = Query(10,ge=1,le=50),user : UserModel = Depends(is_authenticated),db:Session = Depends(get_db)):
    return url_service.get_my_urls(page,limit,user,db)


@url_router.get("/analytics/{url_id}",response_model=UrlAnalyticsSchema,status_code=status.HTTP_200_OK)
def analytics(url_id:int,db:Session=Depends(get_db),user : UserModel = Depends(is_authenticated)):
    return url_service.get_analytics(url_id,db,user)