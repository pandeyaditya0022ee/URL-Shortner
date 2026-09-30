from pwdlib import PasswordHash
from src.utils.settings import settings
from fastapi import HTTPException, status
import jwt
from jwt.exceptions import InvalidTokenError,ExpiredSignatureError

from datetime import datetime, timedelta, timezone
password_hash = PasswordHash.recommended()


def get_password_hash(password):
    return password_hash.hash(password)


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def create_jwt_token(user_id: int, username: str) -> str:
    """Generates a secure JWT token with a 30-minute expiration time."""
    current_time = datetime.now(timezone.utc)
    
    # 2. Define the payload data (Claims)
    payload = {
        "sub": str(user_id),                                      # Subject (the user ID)
        "name": username,                                    # Custom claim
        "iat": current_time,                                 # Issued At time
        "exp": current_time + timedelta(minutes=settings.EXPIRATION_TIME) # Expiration time
    }
    
    # 3. Encode the token
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token

def verify_jwt_token(token: str) -> dict | str:
    """Decodes and validates a JWT token using the secret key."""
    try:
        decoded_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token Expired")
    except jwt.InvalidTokenError as e:
        print("JWT ERROR:", type(e).__name__, str(e))
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token")