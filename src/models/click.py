from sqlalchemy import Column, Integer,String,Boolean,DateTime, ForeignKey
from datetime import datetime
from src.utils.db import Base
from sqlalchemy.orm import relationship




class ClickModel(Base):
    __tablename__ = "click_table"

    id = Column(Integer, primary_key=True)

    url_id = Column(
        Integer,
        ForeignKey("url_table.id", ondelete="CASCADE"),
        nullable=False
    )

    clicked_at = Column(DateTime, default=datetime.now)
    
