from pydantic import BaseModel, ConfigDict
from typing import Optional


class CustomerBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: str
    address: str


class CustomerCreate(CustomerBase):
    pass


class CustomerRead(CustomerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

