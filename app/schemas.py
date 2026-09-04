from pydantic import BaseModel, Field
from datetime import datetime


class AdCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    author: str = Field(..., min_length=1)


class AdUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    author: str | None = None


class AdResponse(BaseModel):
    id: int
    title: str
    description: str
    price: float
    author: str
    creation_date: datetime
