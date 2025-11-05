from sqlalchemy import (
        Column,
        Integer,
        String,
        Float,
        Boolean,
        ForeignKey,
        DateTime,
        Text,
        Enum,
        Date,
        func,
)
from sqlalchemy.orm import relationship
from api.dependencies import Base
import enum

# ENUMS

class OrderStatus(enum.Enum):
    PENDING = "Pending"
    PREPARING = "Preparing"
    OUT_FOR_DELIVERY = "Out for delivery"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

# CUSTOMER MODEL

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(String(255), nullable=False)

    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")


