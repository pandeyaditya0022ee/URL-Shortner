from sqlalchemy import Column, Integer,String,Boolean,DateTime, ForeignKey
from datetime import datetime
from src.utils.db import Base
from sqlalchemy.orm import relationship

class UrlModel(Base):
    __tablename__ = "url_table"
    
    id = Column(Integer,primary_key=True)
    original_url = Column(String,nullable=False)
    short_code = Column(String,unique=True,nullable=False)
    created_at = Column(DateTime,default=datetime.now)
    expires_at = Column(DateTime,nullable=True)
    is_active = Column(Boolean,nullable=False,default=True)
    
    user_id = Column(Integer,ForeignKey ("user_table.id",ondelete="CASCADE"),nullable=False)
    user = relationship("UserModel",back_populates="urls")