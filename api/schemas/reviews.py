from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class ReviewBase(BaseModel):
    order_id: int
    menu_item_id: int
    rating: int
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class ReviewRead(ReviewBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime

