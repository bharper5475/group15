from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "Pending"
    PREPARING = "Preparing"
    OUT_FOR_DELIVERY = "Out for Delivery"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class OrderDetailInline(BaseModel):
    menu_item_id: int
    quantity: int
    item_price: float

class OrderBase(BaseModel):
    tracking_number: str
    customer_id: int
    order_type: str
    total_price: float
    status: Optional[OrderStatus] = OrderStatus.PENDING
    promotion_id: Optional[int] = None
    payment_id: Optional[int] = None

class OrderCreate(OrderBase):
    order_details: List[OrderDetailInline]

class OrderRead(OrderBase):
    id: int
    created_at: datetime
    order_details: List[OrderDetailInline] = []
    class Config: from_attributes = True

