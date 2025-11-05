from sqlalchemy import Column, Integer, String, Float, Boolean, Text
from sqlalchemy.orm import relationship
from api.dependencies.database import Base

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
    recipes = relationship("Recipe", back_populates="menu_item", cascade="all, delete-orphan")

