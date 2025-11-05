from pydantic import BaseModel

class OrderDetailBase(BaseModel):
    order_id: int
    menu_item_id: int
    quantity: int
    item_price: float

class OrderDetailCreate(OrderDetailBase):
    pass

class OrderDetailRead(OrderDetailBase):
    id: int
    class Config: from_attributes = True
