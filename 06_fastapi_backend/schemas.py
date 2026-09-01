from pydantic import BaseModel
from datetime import datetime

class ReportCreate(BaseModel):
    topic: str
    
class ReportResponse(BaseModel):
    id: int
    topic: str
    content: str
    sources: int
    words: int
    created_at: datetime

    class Config:
        from_attributes = True