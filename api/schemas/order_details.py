from pydantic import BaseModel, ConfigDict


class OrderDetailBase(BaseModel):
    order_id: int
    menu_item_id: int
    quantity: int
    item_price: float


class OrderDetailCreate(OrderDetailBase):
    pass


class OrderDetailRead(OrderDetailBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
