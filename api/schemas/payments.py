from pydantic import BaseModel
from typing import Optional

class PaymentBase(BaseModel):
    payment_type: str
    status: str
    amount: float
    masked_card_last4: Optional[str] = None
    transaction_id: Optional[str] = None

class PaymentCreate(PaymentBase):
    pass

class PaymentRead(PaymentBase):
    id: int
    class Config: from_attributes = True

