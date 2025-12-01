from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Optional
from datetime import datetime
from enum import Enum


class OrderStatus(str, Enum):
    RECEIVED = "RECEIVED"
    PENDING = "PENDING"
    PREPARING = "PREPARING"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


# What the client sends for each item when creating an order
class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int = Field(gt=0, description="Quantity must be a positive integer")


# What we return for each order detail item
class OrderDetailInline(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    menu_item_id: int
    quantity: int
    item_price: float


# Request body for POST /orders
class OrderCreate(BaseModel):
    # Either customer_id OR guest info must be provided
    customer_id: Optional[int] = None

    guest_name: Optional[str] = None
    guest_phone: Optional[str] = None
    guest_address: Optional[str] = None

    order_type: str  # "takeout" or "delivery"
    order_items: List[OrderItemCreate]
    promotion_code: Optional[str] = None

    # Validate order type
    @field_validator("order_type")
    @classmethod
    def validate_order_type(cls, v: str) -> str:
        allowed = {"takeout", "delivery"}
        if v.lower() not in allowed:
            raise ValueError(f"order_type must be one of {allowed}")
        return v.lower()

    # Validate items list not empty
    @field_validator("order_items")
    @classmethod
    def validate_items_not_empty(
        cls, v: List[OrderItemCreate]
    ) -> List[OrderItemCreate]:
        if not v:
            raise ValueError("order_items must contain at least one item")
        return v

    # Validate identity requirement for guest checkout
    @field_validator("guest_address", mode="after")
    @classmethod
    def validate_guest_or_customer(cls, _, values):
        customer_id = values.get("customer_id")
        guest_name = values.get("guest_name")
        guest_phone = values.get("guest_phone")
        guest_address = values.get("guest_address")

        # Case 1: Registered customer placing order → OK
        if customer_id is not None:
            return _

        # Case 2: Guest checkout → require name, phone, address
        if guest_name and guest_phone and guest_address:
            return _

        raise ValueError(
            "Either customer_id OR guest_name, guest_phone, and guest_address must be provided"
        )


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
    model_config = ConfigDict(from_attributes=True)

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
