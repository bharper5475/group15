from pydantic import BaseModel
from datetime import date
from typing import Optional

class PromotionBase(BaseModel):
    code: str
    discount_percent: float
    expiration_date: date
    is_active: Optional[bool] = True

class PromotionCreate(PromotionBase):
    pass

class PromotionRead(PromotionBase):
    id: int
    class Config: from_attributes = True

