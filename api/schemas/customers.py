from pydantic import BaseModel
from typing import Optional

class CustomerBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: str
    address: str

class CustomerCreate(CustomerBase):
    pass

class CustomerRead(CustomerBase):
    id: int
    class Config: from_attributes = True

