from pydantic import BaseModel, ConfigDict
from typing import Optional


class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    calories: Optional[int] = None
    category: Optional[str] = None
    is_available: Optional[bool] = True


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemRead(MenuItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

