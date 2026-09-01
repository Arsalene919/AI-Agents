from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    
class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ReportCreate(BaseModel):
    topic: str
    
class ReportResponse(BaseModel):
    id: int
    topic: str
    content: str
    sources: Optional[int] = 0
    words: Optional[int] = 0
    created_at: datetime

    class Config:
        from_attributes = True