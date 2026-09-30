from sqlalchemy import Column, Integer,String,Boolean,DateTime
from datetime import datetime
from src.utils.db import Base
from sqlalchemy.orm import relationship

class UserModel(Base):
    __tablename__ = "user_table"
    
    id = Column(Integer,primary_key=True)
    username = Column(String,unique=True,nullable=False)
    email = Column(String,nullable=False,unique=True)
    hash_password = Column(String,nullable=False)
    created_at = Column(DateTime,default=datetime.now)
    
    
    
    urls = relationship("UrlModel",back_populates="user")