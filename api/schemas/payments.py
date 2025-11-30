from pydantic import BaseModel, ConfigDict
from typing import Optional


class PaymentBase(BaseModel):
    payment_type: str
    status: str
    amount: float
    masked_card_last4: Optional[str] = None
    transaction_id: Optional[str] = None


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    payment_type: Optional[str] = None
    status: Optional[str] = None
    amount: Optional[float] = None
    masked_card_last4: Optional[str] = None
    transaction_id: Optional[str] = None


class PaymentRead(PaymentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

