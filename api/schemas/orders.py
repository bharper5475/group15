from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime
from enum import Enum


class OrderStatus(str, Enum):
    RECEIVED = "Received"
    PENDING = "Pending"
    PREPARING = "Preparing"
    OUT_FOR_DELIVERY = "Out for Delivery"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


# What the client sends for each item when creating an order
class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int = Field(gt=0, description="Quantity must be a positive integer")


# What we return for each order detail item
class OrderDetailInline(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    item_price: float

    class Config:
        from_attributes = True


# Request body for POST /orders
class OrderCreate(BaseModel):
    customer_id: int
    order_type: str  # "takeout" or "delivery"
    order_items: List[OrderItemCreate]
    promotion_code: Optional[str] = None

    @field_validator("order_type")
    @classmethod
    def validate_order_type(cls, v: str) -> str:
        allowed = {"takeout", "delivery"}
        if v.lower() not in allowed:
            raise ValueError(f"order_type must be one of {allowed}")
        return v.lower()

    @field_validator("order_items")
    @classmethod
    def validate_items_not_empty(
        cls, v: List[OrderItemCreate]
    ) -> List[OrderItemCreate]:
        if not v:
            raise ValueError("order_items must contain at least one item")
        return v


# Request body for PUT /orders/{id}
class OrderUpdate(BaseModel):
    order_type: Optional[str] = None
    status: Optional[OrderStatus] = None

    @field_validator("order_type")
    @classmethod
    def validate_order_type(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        allowed = {"takeout", "delivery"}
        if v.lower() not in allowed:
            raise ValueError(f"order_type must be one of {allowed}")
        return v.lower()


# Response model for GET/POST/PUT /orders
class OrderRead(BaseModel):
    id: int
    tracking_number: str
    customer_id: int
    order_type: str
    total_price: float
    status: OrderStatus
    promotion_id: Optional[int] = None
    payment_id: Optional[int] = None
    created_at: datetime
    order_details: List[OrderDetailInline] = []

    class Config:
        from_attributes = True

