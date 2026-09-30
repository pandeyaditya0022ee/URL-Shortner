from pydantic import BaseModel
from datetime import datetime

class UserRegisterSchema(BaseModel):
    username : str
    email : str
    password : str
    
class UserResponseSchema(BaseModel):
    username : str
    email : str
    created_at : datetime
    
    
class LoginSchema(BaseModel):
    username : str
    password : str

class TokenResponseSchema(BaseModel):
    access_token : str
    token_type : str