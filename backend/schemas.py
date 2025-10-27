from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProductCreate(BaseModel):
    name: str
    sku: str
    description: Optional[str] = None
    price: float = Field(..., ge=0)
    quantity: int = Field(..., ge=0)
    is_active: Optional[bool] = True

class ProductUpdate(BaseModel):
    name: Optional[str]
    sku: Optional[str]
    description: Optional[str]
    price: Optional[float]
    quantity: Optional[int]
    is_active: Optional[bool]

class ProductOut(BaseModel):
    id: int
    name: str
    sku: str
    description: Optional[str]
    price: float
    quantity: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
