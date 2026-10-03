from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt

from src.utils.db import get_db
from src.utils.security import verify_jwt_token
from src.models.user import UserModel
from fastapi import Request, HTTPException, status
from src.utils.redis_client import redis_client
from src.utils.logger import logger


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")




def is_authenticated(token : str = Depends(oauth2_scheme),db:Session = Depends(get_db)):
    try:
        payload = verify_jwt_token(token)
        user_id = int(payload.get("sub"))
        
        if not user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found")
        
        user_id = int(user_id)
        user : UserModel = db.query(UserModel).filter(UserModel.id == user_id).first()
        
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found")
        
        return user
    
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token")
    
    

def rate_limit(request: Request):
    ip = request.client.host

    key = f"rate_limit:{ip}"

    count = redis_client.incr(key)

    if count == 1:
        redis_client.expire(key, 60)

    if count > 10:
        logger.warning(
            "Rate limit exceeded | ip=%s",
            ip,
        )
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests"
        )