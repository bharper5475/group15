from pydantic import BaseModel
from datetime import datetime, date
from typing import List, Optional
from enum import Enum


# ENUM
class OrderStatus(str, Enum):
    PENDING = "Pending"
    PREPARING = "Preparing"
    OUT_FOR_DELIVERY = "Out for Delivery"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

# CUSTOMER
class CustomerBase(BaseModel):
    name: str
    phone: str
    address: str


class CustomerCreate(CustomerBase):
    pass


class CustomerRead(CustomerBase):
    id: int

    class Config:
        orm_mode = True
