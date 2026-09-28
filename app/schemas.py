from pydantic import BaseModel, Field
from typing import Optional

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    category: str = Field(..., min_length=1)
    stock: int = Field(default=0, ge=0)

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1)
    stock: Optional[int] = Field(None, ge=0)

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    category: str
    stock: int

    class Config:
        from_attributes = True