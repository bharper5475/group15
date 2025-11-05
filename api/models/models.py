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

# MENU ITEM MODEL 

class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    calories = Column(Integer, nullable=True)
    category = Column(String(50), nullable=True) 
    is_available = Column(Boolean, default=True)

    order_details = relationship("OrderDetail", back_populates="menu_item", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="menu_item", cascade="all, delete-orphan")

# PROMOTION MODEL

class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False)
    discount_percent = Column(Float, nullable=False)
    expiration_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)

    orders = relationship("Order", back_populates="promotion")
