from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    sources = Column(Integer, default=0)
    words = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())