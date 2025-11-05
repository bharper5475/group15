from sqlalchemy import Column, Integer, String, Float
from api.dependencies.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    payment_type = Column(String(30), nullable=False)     
    status = Column(String(30), nullable=False)           
    masked_card_last4 = Column(String(4), nullable=True)
    transaction_id = Column(String(100), nullable=True)
    amount = Column(Float, nullable=False)

