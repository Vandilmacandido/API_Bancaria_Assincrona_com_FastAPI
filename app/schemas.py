from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Transaction Schemas
class TransactionBase(BaseModel):
    amount: float

class TransactionCreate(TransactionBase):
    pass # Type is handled by endpoint logic

class TransactionResponse(TransactionBase):
    id: int
    type: str
    timestamp: datetime
    
    class Config:
        from_attributes = True

# User Schemas
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    balance: float
    transactions: List[TransactionResponse] = []

    class Config:
        from_attributes = True
