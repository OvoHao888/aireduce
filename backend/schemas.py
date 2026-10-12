from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List, Optional

class UserRegister(BaseModel):
    username: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    expire_date: Optional[datetime]
    total_usage: int
    member_level: Optional[str]
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class CardExchange(BaseModel):
    card_code: str = Field(..., min_length=8, max_length=32)

class CardExchangeResponse(BaseModel):
    success: bool
    message: str
    token_type: Optional[str]
    duration_days: Optional[int]
    duration_hours: Optional[int]
    new_expire_date: Optional[datetime]

class ProductResponse(BaseModel):
    id: int
    name: str
    token_type: str
    duration_hours: Optional[int]
    duration_days: Optional[int]
    price: Optional[float]
    original_price: Optional[float]
    description: Optional[str]
    is_active: Optional[bool] = True
    sort_order: Optional[int] = 0
    
    class Config:
        from_attributes = True

class ProcessRequest(BaseModel):
    text: str
    mode: str = Field(..., pattern="^(mode1|mode2)$")
    # AI API配置
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = 1.0
    max_tokens: Optional[int] = 4000

class ProcessResponse(BaseModel):
    success: bool
    message: str
    output_text: Optional[str]
    record_id: Optional[int]

class UsageRecordResponse(BaseModel):
    id: int
    mode: str
    input_text: str
    output_text: Optional[str]
    status: str
    error_message: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class UsageRecordListResponse(BaseModel):
    records: List[UsageRecordResponse]
    total: int
    page: int
    limit: int

class FeedbackRequest(BaseModel):
    content: str
    contact: Optional[str] = None
    type: str = Field(..., pattern="^(suggestion|bug|complaint|other)$")

class FeedbackResponse(BaseModel):
    id: int
    content: str
    contact: Optional[str]
    type: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True