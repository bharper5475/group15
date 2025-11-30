from pydantic import BaseModel, ConfigDict
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
    model_config = ConfigDict(from_attributes=True)

    id: int

